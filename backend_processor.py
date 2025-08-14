# This file orchestrates the entire process from prompt to video,
# including the plan-and-debug loop.
import subprocess
import tempfile
from pathlib import Path
import os
import numpy as np
import time
import shutil
from tools import (
    create_animation_plan,
    create_manim_code,
    debug_manim_code
)

# Define a constant for the maximum number of debug attempts.
MAX_DEBUG_ATTEMPTS = 3

def _render_manim_video(manim_code: str, attempt: int, quality: str) -> Path:
    """
    Internal helper function to save Manim code to a file and render it.
    This function is called by the main processing loop.

    Args:
        manim_code: The Python script string to be rendered.
        attempt: The current attempt number (for logging purposes).

    Returns:
        The Path object pointing to the successfully rendered MP4 video file.

    Raises:
        RuntimeError: If the Manim process fails, this exception is raised
                      containing the stderr output from Manim.
    """
    
    # --- This dictionary maps the user's choice to Manim's command-line flags for quality---
    quality_dict = {
        "480p": "-ql",
        "720p": "-qm",
        "1080p": "-qh",
        "2160p": "-qk"
    }

    # --- This dictionary maps the flags to Manim's output folder names ---
    quality_folders = {
        "480p": "480p15",
        "720p": "720p30",
        "1080p": "1080p60",
        "2160p": "2160p60"
    }

    # Use a temporary file to store the Manim script.
    #This block takes the code string and saves it into a real Python file.
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as temp_script:
        temp_script.write(manim_code)
        script_path = Path(temp_script.name)

    # Here dir is created where all the files of manim will be stored(videos/images/logs)
    print(f"--- [Attempt {attempt}] Rendering script: {script_path} with quality '{quality}'")
    media_dir = Path.cwd() / "temp_media"
    media_dir.mkdir(exist_ok = True)

    # Construct the command to run Manim from the command line.
    #This block builds the command-line instruction to render the video.
    command = [
        "manim", str(script_path), "GeneratedScene", "--format=mp4",
        quality_dict[quality],  # Render in quick, low quality for speed.
        "--media_dir", str(media_dir)
    ]

    # This block executes the command and, if it works, finds and returns the path to the new video file.
    try:
        # Execute the Manim command.
        process = subprocess.run(
            command,
            check=True, # This will raise CalledProcessError on a non-zero exit code.
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        # Find the generated video file.
        video_dir = media_dir / "videos" / script_path.stem / quality_folders[quality]
        video_files = list(video_dir.glob("*.mp4"))

        if not video_files:
            raise FileNotFoundError("Manim executed successfully but did not produce a video file.")

        print(f"--- [Attempt {attempt}] Render SUCCESSFUL.")
        return video_files[0]

    # If Manim fails, this block catches the technical error message and passes it up the chain.
    except subprocess.CalledProcessError as e:
        # This is the primary failure case for broken code.
        print(f"--- [Attempt {attempt}] Render FAILED.")
        # Re-raise a new exception containing Manim's specific error message.
        raise RuntimeError(e.stderr) from e

    finally:
        # Ensure the temporary script file is always cleaned up.
        if script_path.exists():
            os.remove(script_path)


def process_prompt_to_video(prompt: str, quality: str) -> Path:
    """
    This is the main entry point function for the backend.
    It receives the user's query and orchestrates the full "Plan-and-Debug" pipeline.

    Args:
        prompt: The natural language animation description from the user.

    Returns:
        The Path object to the final, successfully rendered MP4 video.

    Raises:
        RuntimeError: If the pipeline fails after all debug attempts.
    """
    print(f"\n--- NEW JOB: PROCESSING PROMPT: '{prompt}' ---")

    temp_media_dir = Path.cwd() / "temp_media"

    # === STEP 1: PLAN ===
    # Call the Planner agent to create a detailed plan.
    plan = create_animation_plan(prompt)

    # === STEP 2: CODE ===
    # Call the Coder agent to generate the initial Manim script based on the plan.
    current_code = create_manim_code(plan)

    # === STEP 3: RENDER & DEBUG LOOP ===
    # This loop will try to render the code, and if it fails, it will call the
    # Debugger agent and try again with the corrected code.
    try:
        for attempt in range(1, MAX_DEBUG_ATTEMPTS + 1):
            try:
                # Attempt to render the current version of the code.
                temp_video_path = _render_manim_video(current_code, attempt, quality)

                # This block runs only on success. It copies the temporary video
                # to a permanent location before the temp folder is deleted.
                final_output_dir = Path.cwd() / "final_videos"
                final_output_dir.mkdir(exist_ok=True)
                
                # Create a unique filename using a timestamp to prevent overwrites
                unique_filename = f"{os.path.splitext(temp_video_path.name)[0]}_{int(time.time())}.mp4"
                final_video_path = final_output_dir / unique_filename
                
                # Copy the file
                shutil.copy(temp_video_path, final_video_path)

                # If rendering is successful, the loop is exited and the video path is returned.
                print("--- PIPELINE COMPLETED SUCCESSFULLY ---")
                return final_video_path

            except Exception as e:
                # This block catches the RuntimeError from the render function.
                error_message = str(e)
                print(f"--- ERROR caught on attempt {attempt}. Preparing to debug.")

                # === FALLBACK LOGIC ===
                # If we have reached the maximum number of attempts, we give up.
                if attempt == MAX_DEBUG_ATTEMPTS:
                    print("--- Max debug attempts reached. Aborting pipeline.")
                    # Raise a final, user-friendly error.
                    raise RuntimeError(
                        f"Failed to generate video after {MAX_DEBUG_ATTEMPTS} attempts. "
                        f"The request may be too complex. Last error: {error_message}"
                    )

                # If we still have attempts left, call the Debugger agent.
                print("--- Calling Debugger LLM for a fix...")
                current_code = debug_manim_code(
                    plan = plan,
                    broken_code = current_code,
                    error_message = error_message
                )
                # The loop will now continue to the next iteration with the newly corrected code.

    finally:
        # This `finally` block ensures that the temporary media directory
        # is ALWAYS deleted after the job is finished, whether it succeeded or failed.
        # The `final_videos` folder is NOT touched.
        if temp_media_dir.exists():
            print(f"--- Cleaning up temporary directory: {temp_media_dir} ---")
            shutil.rmtree(temp_media_dir)

    raise RuntimeError("Exited the debug loop unexpectedly.")

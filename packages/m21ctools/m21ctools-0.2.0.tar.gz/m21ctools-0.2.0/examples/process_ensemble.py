# Ensemble Spread Test with mock data
# Run generate_mock python scripts first

import sys
import os
from datetime import datetime
import time
import icechunk
import matplotlib.pyplot as plt

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

import m21ctools.data_handler as m21c_handler
import m21ctools.config as cfg

##### Test Configuration #####

MOCK_DATA_SCRIPT = "../notebooks/scripts/generate_mock1.py" 
MOCK_DATA_DIR = "../mock_data" 
TEST_REPO_PATH = "./test_ensemble_store_integration" 
TEST_PLOT_DIR = "./test_plots" 

TEST_START_DATE = datetime(2010, 1, 1, 0)
TEST_END_DATE = datetime(2010, 1, 2, 0)

# Variables to process
VAR3D_TEST = ['u']
VAR2D_TEST = ['ps']

NUM_WORKERS_TEST = 4 
FORCE_RERUN_TEST = True # Set to True to ensure processing happens for the test

##### End Test Configuration #####


def run_test():
    print("--- Starting Integration Test ---")
    start_time_script = time.time()

    print(f"Checking/Generating mock data using {MOCK_DATA_SCRIPT}...")
    if not os.path.exists(MOCK_DATA_DIR):
        print("Running mock data generation script...")
        os.system(f"python {MOCK_DATA_SCRIPT}")
        print("Mock data script finished.")
    else:
        print(f"Mock data directory '{MOCK_DATA_DIR}' already exists.")


    print("Overriding config paths for test environment...")
    original_input_path = cfg.BASE_INPUT_PATH
    original_plot_path = cfg.BASE_OUTPUT_PLOT_PATH
    cfg.BASE_INPUT_PATH = MOCK_DATA_DIR 
    cfg.BASE_OUTPUT_PLOT_PATH = TEST_PLOT_DIR 

    os.makedirs(TEST_REPO_PATH, exist_ok=True)
    os.makedirs(TEST_PLOT_DIR, exist_ok=True)

    print(f"Using test icechunk repository: {TEST_REPO_PATH}")

    # Clean up old test repo first and setup new test repo
    import shutil
    if os.path.exists(TEST_REPO_PATH):
        shutil.rmtree(TEST_REPO_PATH)

    storage = icechunk.local_filesystem_storage(TEST_REPO_PATH)
    repo = icechunk.Repository.open_or_create(storage)

    # Determine skip times (not needed if test repo is clean/force=True)
    times_to_skip = set()
    if not FORCE_RERUN_TEST and (VAR3D_TEST + VAR2D_TEST):
        try:
            check_var = (VAR3D_TEST + VAR2D_TEST)[0]
            times_to_skip = m21c_handler.get_existing_times(repo, check_var)
            print(f"Found {len(times_to_skip)} existing timestamps for '{check_var}'.")
        except Exception: pass
    else:
        print("Force rerun is ON or no variables to check, processing all.")


    # Run processing
    print(f"Running parallel processing for range {TEST_START_DATE} to {TEST_END_DATE}...")
    combined_averages = m21c_handler.parallel_process_files_2d3d(
        TEST_START_DATE, TEST_END_DATE,
        VAR3D_TEST, VAR2D_TEST,
        skip_times=times_to_skip,
        num_workers=NUM_WORKERS_TEST,
        force_rerun=FORCE_RERUN_TEST
    )

    # Save Results to test repo
    # if not combined_averages or all(not v for v in combined_averages.values()):
    if not combined_averages or all(v.size == 0 for v in combined_averages.values()):
        print("No data processed to save.")
    else:
        print("Saving processed data to test icechunk repo...")
        commit_message = f"Integration test run: {TEST_START_DATE} to {TEST_END_DATE}"
        m21c_handler.save_to_icechunk(repo, combined_averages, commit_message)
        print("Data saved.")

        print("Loading data back from test repo and plotting...")
        plot_generated = False
        if 'u' in VAR3D_TEST:
            try:
                u_data = m21c_handler.load_from_icechunk(repo, 'u')
                print("Plotting u_data...")
                m21c_handler.plot_hovmoeller_3d(u_data, var='u') # saving to TEST_PLOT_DIR
                plot_generated = True
            except Exception as e:
                print(f"Could not load/plot 'u': {e}")
        if 'ps' in VAR2D_TEST:
             try:
                ps_data = m21c_handler.load_from_icechunk(repo, 'ps')
                print("Plotting ps_data...")
                m21c_handler.plot_hovmoeller_2d(ps_data, var='ps') # saving to TEST_PLOT_DIR
                plot_generated = True
             except Exception as e:
                print(f"Could not load/plot 'ps': {e}")

        if plot_generated:
            print(f"Plots saved in: {os.path.abspath(TEST_PLOT_DIR)}")
            plt.close('all')

    cfg.BASE_INPUT_PATH = original_input_path
    cfg.BASE_OUTPUT_PLOT_PATH = original_plot_path
    print("Restored original config paths.")

    print(f"--- Test Finished in {time.time() - start_time_script:.2f} seconds ---")

if __name__ == "__main__":
    run_test()
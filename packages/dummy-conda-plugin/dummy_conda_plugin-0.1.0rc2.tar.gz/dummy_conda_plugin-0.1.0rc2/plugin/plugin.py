import subprocess, sys, pkg_resources, os
from conda import plugins
from conda.base.context import context

def package_counter(command: str):
    """Displays the total number of packages in the environment"""
    target_prefix = context.target_prefix
    try:
        install_dataflow_deps = pkg_resources.resource_filename('plugin', 'scripts/install_dataflow_deps.sh')
        os.chmod(install_dataflow_deps, 0o755)
        process = subprocess.Popen(
            ["bash", install_dataflow_deps, target_prefix],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        for line in iter(process.stdout.readline, ''):
            print(line, end='')
            sys.stdout.flush()
        
        return_code = process.wait()
        if return_code != 0:
            print(f"Error in creating environment!!")
        
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


    
@plugins.hookimpl
def conda_post_commands():
    yield plugins.CondaPostCommand(
        name=f"package_counter_post_command",
        action=package_counter,
        run_for={"create"},
    )
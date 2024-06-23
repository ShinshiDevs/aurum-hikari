import os
import platform

from aurum import _about

if __name__ == "__main__":
    print(
        f"Aurum {_about.__version__} located at {os.path.abspath(os.path.dirname(_about.__file__))} \n"
        f"{platform.python_implementation()} {platform.python_version()} {platform.python_compiler()} \n"
        f"{platform.uname().version} {platform.platform()}"
    )

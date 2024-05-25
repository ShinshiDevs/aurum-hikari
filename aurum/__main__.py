import os
import platform

from aurum import _about

if __name__ == "__main__":
    print(
        f"Aurum {_about.__version__} located on {os.path.abspath(os.path.dirname(_about.__file__))}",
        f"{platform.python_implementation()} {platform.python_version()} {platform.python_compiler()}",
        f"{platform.uname().version} {platform.platform()}",
        sep="\n",
    )

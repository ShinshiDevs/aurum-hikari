import os
import platform

from aurum import _about as about_aurum
from hikari import _about as about_hikari

if __name__ == "__main__":
    print(
        f"Aurum {about_aurum.__version__} located at {os.path.abspath(os.path.dirname(about_aurum.__file__))} \n"
        f"hikari {about_hikari.__version__} \n"
        f"{platform.python_implementation()} {platform.python_version()} {platform.python_compiler()} \n"
        f"{platform.uname().version} {platform.platform()}"
    )

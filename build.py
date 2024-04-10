import os
import shutil
from distutils.core import Distribution, Extension

from Cython.Build import build_ext, cythonize

cython_dir = os.path.join("graph_ml", "_ext")
extension = Extension(
    "graph_ml.cytrie",
    [
        os.path.join(cython_dir, "cytrie.pyx"),
    ],
    extra_compile_args=["-O3", "-std=c++17"],
)

ext_modules = cythonize([extension], include_path=[cython_dir])
dist = Distribution({"ext_modules": ext_modules})
cmd = build_ext(dist)
cmd.ensure_finalized()
cmd.run()

for output in cmd.get_outputs():
    relative_extension = os.path.relpath(output, cmd.build_lib)
    shutil.copyfile(output, relative_extension)
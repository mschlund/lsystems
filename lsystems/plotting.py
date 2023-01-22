import os
import shutil
import numpy as np


def draw_random_curves(Curve, base_dir, num_curves=20, random_seed=42, max_iters=4):
    # Generation of random curves

    if os.path.exists(base_dir):
        rename_str = base_dir + "_BAK"
        if os.path.exists(rename_str):
            shutil.rmtree(rename_str)
        os.rename(base_dir, rename_str)

    os.mkdir(base_dir)

    c = Curve()
    chars = list(set(c.postProcessMap.keys()).union(set(c.get_constants())))
    rng = np.random.default_rng(random_seed)  # fixed random-seed for reproducibility

    for i in range(num_curves):
        start_string = "".join(rng.choice(chars, size=10))
        for iters in range(max_iters):
            filename = base_dir + "/" + start_string + f"_iters{iters}" + ".svg"
            c = Curve(width=5, filename=filename)
            c.run_curved(iters=iters, init_str=start_string, writeOutput=True)

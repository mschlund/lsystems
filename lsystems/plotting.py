import os
import shutil
import numpy as np
import matplotlib.pyplot as plt
import cairosvg

import PIL
import io


def draw_random_curves(Curve, base_dir, num_curves=20, random_seed=42, max_iters=4, curved=False):
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
        try:
            start_string = "".join(rng.choice(chars, size=10))
            n_rows = 3
            n_cols = 2

            fig, ax = plt.subplots(nrows=n_rows, ncols=n_cols)
            filename = base_dir + "/" + start_string + ".svg"

            for iters in range(max_iters+1):
                c = Curve()
                if curved:
                    svg_string = c.run_curved(iters=iters, init_str=start_string)
                else:
                    svg_string = c.run_str(iters=iters, init_str=start_string)
                row = int(iters / n_cols)
                col = iters % n_cols
                img_png = cairosvg.svg2png(svg_string)
                img = PIL.Image.open(io.BytesIO(img_png))
                ax[row, col].imshow(img)

            fig.savefig(filename)
            plt.close()

        except:
            pass

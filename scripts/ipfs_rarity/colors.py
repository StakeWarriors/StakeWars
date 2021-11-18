import os
import random
import webcolors
import numpy as np
from sklearn.metrics import mean_squared_error
import colorsys
from PIL import Image, ImageSequence


def colors_in_image(file_path):
    img = Image.open(file_path)
    colors = img.convert("RGB").getcolors()
    return colors


def hex_to_name(c):
    h_color = "#{:02x}{:02x}{:02x}".format(int(c[0]), int(c[1]), int(c[2]))
    try:
        nm = webcolors.hex_to_name(h_color, spec="css3")
    except ValueError as v_error:
        rms_lst = []
        for img_clr, img_hex in webcolors.CSS3_NAMES_TO_HEX.items():
            cur_clr = webcolors.hex_to_rgb(img_hex)
            rmse = np.sqrt(mean_squared_error(c, cur_clr))
            rms_lst.append(rmse)

        closest_color = rms_lst.index(min(rms_lst))

        nm = list(webcolors.CSS3_NAMES_TO_HEX.items())[closest_color][0]
    return nm


rgb_to_hsv = np.vectorize(colorsys.rgb_to_hsv)
hsv_to_rgb = np.vectorize(colorsys.hsv_to_rgb)


def shift_hue(arr, hout):
    r, g, b, a = np.rollaxis(arr, axis=-1)
    if hout == 0:
        return np.dstack((r, g, b, a))
    elif hout == 1:
        return np.dstack((r, b, g, a))
    elif hout == 2:
        return np.dstack((b, r, g, a))
    elif hout == 3:
        return np.dstack((b, g, r, a))
    elif hout == 4:
        return np.dstack((g, b, r, a))
    elif hout == 5:
        return np.dstack((g, r, b, a))
    else:
        if max(r, g, b) == r:
            if b > g:
                return np.dstack((g, b, g, a))
            else:
                return np.dstack((b, b, g, a))
        elif max(r, g, b) == b:
            if r > g:
                return np.dstack((b, b, r, a))
            else:
                return np.dstack((r, r, g, a))
        else:
            if r > b:
                return np.dstack((r, r, b, a))
            else:
                return np.dstack((r, b, r, a))


def colorize(image, hue):
    """
    Colorize PIL image `original` with the given
    `hue` (hue within 0-360); returns another PIL image.
    """
    img = image.convert("RGBA")
    arr = np.array(np.asarray(img).astype("float"))
    new_img = Image.fromarray(shift_hue(arr, hue).astype("uint8"), "RGBA")

    return new_img


def create_gif_frame(frame, transparency=255):
    # 'only RGB or L mode images can be quantized to a palette' says PIL
    quantized = (frame.convert("RGB") if frame.mode != "RGB" else frame).quantize(
        colors=255, method=2, kmeans=0, dither=0
    )
    # Save the transparency areas beforehand because quantizing doesn't always respect it
    mask = (
        np.array(frame.convert("RGBA") if frame.mode != "RGBA" else frame.copy())[
            :, :, 3
        ].copy()
        // 255
    )
    # Puts back the transparency areas on the image after quantization
    data = np.array(quantized)
    data = data * mask  # Nullifies transparent areas
    mask = -(mask - 1) * transparency
    data = data + mask  # Makes transparent area the transparency color
    result = Image.fromarray(data, "P")
    result.putpalette(quantized.getpalette())
    result.info["transparency"] = transparency
    return result


def create_variant(og_file_path, new_file_path, hue_shift):
    with Image.open(og_file_path, "r") as image:

        frames, durations = [], []
        for frame in ImageSequence.Iterator(image):
            colored_frame = colorize(frame, hue_shift)
            new_frame = create_gif_frame(colored_frame)
            frames.append(new_frame)
            # crucial to get duration+timestamp
            image.copy()
            duration = image.info.get("duration")
            assert (
                duration is None or type(duration) is int
            )  # 'image/mpo' has no duration
            if duration is None:
                assert not durations
                break
            durations.append(duration)
        frames[0].save(
            new_file_path,
            format="GIF",
            version="GIF89a",
            save_all=True,
            optimize=False,
            disposal=2,
            append_images=frames[1:],
            duration=durations,
            loop=0,
        )


def get_traits(token_img):
    colors = colors_in_image(token_img)
    traits = []
    sets = set()
    for i in range(len(colors)):
        (trait, value) = color_remapping(hex_to_name(colors[i][1]))
        if trait not in sets:
            sets.add(trait)
            traits.append({"field": trait, "degree": value})
    return traits


def color_remapping(color):
    value = random.randint(0, 1000)
    value = float(float(value) / 1000)
    if color == "burlywood":
        return ("Civilian Murderer", int(value * 100))
    elif color == "cadetblue":
        return ("Unwavering", value * 100)
    elif color == "chocolate":
        return ("Sweetheart", value * 100)
    elif color == "cornflowerblue":
        return ("Illiterate", 0)
    elif color == "cyan":
        return ("Has child(ren)", int(value * 5))
    elif color == "darkcyan":
        return ("Abandoned as a child", 0)
    elif color == "darkgoldenrod":
        return ("Dark Legion Member", 0)
    elif color == "darkgray":
        return ("Musical", value * 100)
    elif color == "darkgreen":
        return ("Has sibling(s)", int(value * 5))
    elif color == "darkkhaki":
        return ("Respected", value * 100)
    elif color == "darkmagenta":
        return ("Ugly", value * 100)
    elif color == "darkolivegreen":
        return ("Honorable", value * 100)
    elif color == "darkred":
        return ("Merciless", value * 100)
    elif color == "darksalmon":
        return ("Bodacious", value * 100)
    elif color == "darkslateblue":
        return ("Family Focused", value * 100)
    elif color == "darkslategray":
        return ("Caring", value * 100)
    elif color == "dimgray":
        return ("Deceitful", value * 100)
    elif color == "dodgerblue":
        return ("Wealthy", value * 100)
    elif color == "firebrick":
        return ("Poor", value * 100)
    elif color == "forestgreen":
        return ("Attractive", value * 100)
    elif color == "gainsboro":
        return ("Was drafted into war at a young age", int(value * 10 - 1) + 7)
    elif color == "gold":
        return ("Ruler", 0)
    elif color == "goldenrod":
        return ("Devoted", value * 100)
    elif color == "gray":
        return ("Religious", value * 100)
    elif color == "greenyellow":
        return ("Exhausted", value * 100)
    elif color == "hotpink":
        return ("Cute", value * 100)
    elif color == "indianred":
        return ("Alcoholic", value * 100)
    elif color == "khaki":
        return ("Patient", value * 100)
    elif color == "lightcoral":
        return ("Innocent", value * 100)
    elif color == "lightcyan":
        return ("Naive", value * 100)
    elif color == "lightgray":
        return ("Honest", value * 100)
    elif color == "lightseagreen":
        return ("Authentic", value * 100)
    elif color == "lightsteelblue":
        return ("Only wants to return home", 0)
    elif color == "maroon":
        return ("Only looking for love", 0)
    elif color == "mediumblue":
        return ("Criminal", 0)
    elif color == "mediumorchid":
        return ("Slaver", 0)
    elif color == "mediumpurple":
        return ("Royalty", 0)
    elif color == "mediumslateblue":
        return ("Tired of living", value * 100)
    elif color == "mediumvioletred":
        return ("Sinister", value * 100)
    elif color == "midnightblue":
        return ("Loves to cook", 0)
    elif color == "navajowhite":
        return ("Just wants to be loved", 0)
    elif color == "navy":
        return ("Single", 0)
    elif color == "olive":
        return ("Lost their parents", 0)
    elif color == "olivedrab":
        return ("Married", 0)
    elif color == "orange":
        return ("Killed their lover", 0)
    elif color == "orangered":
        return ("Lives with unspeakable regret", 0)
    elif color == "orchid":
        return ("Searching for their lost lover", 0)
    elif color == "palevioletred":
        return ("Depressed", value * 100)
    elif color == "peru":
        return ("Intense", value * 100)
    elif color == "plum":
        return ("Quiet", value * 100)
    elif color == "powderblue":
        return ("Clever", value * 100)
    elif color == "royalblue":
        return ("Punctual", value * 100)
    elif color == "saddlebrown":
        return ("Dissociated", value * 100)
    elif color == "sandybrown":
        return ("Intrusive", value * 100)
    elif color == "seagreen":
        return ("Forest Dweller", 0)
    elif color == "sienna":
        return ("Short Tempered", value * 100)
    elif color == "silver":
        return ("Ancient", int(value * 10000))
    elif color == "slateblue":
        return ("Esteemed", value * 100)
    elif color == "teal":
        return ("Eerie", value * 100)
    elif color == "thistle":
        return ("Pure", value * 100)
    elif color == "turquoise":
        return ("Majestic", value * 100)
    elif color == "violet":
        return ("Arrogant", value * 100)
    else:
        value2 = random.randint(0, 10)
        if value2 == 0:
            return ("Heroic", value * 100)
        elif value2 == 1:
            return ("Villainous", value * 100)
        elif value2 == 2:
            return ("Pacifist", value * 100)
        elif value2 == 3:
            return ("Cowardice", value * 100)
        elif value2 == 4:
            return ("Lazy", value * 100)
        elif value2 == 5:
            return ("Confused", value * 100)
        elif value2 == 6:
            return ("Social", value)
        elif value2 == 7:
            return ("Chaotic", value)
        elif value2 == 8:
            return ("Lawful", value)
        elif value2 == 9:
            return ("Silly", value)
        else:
            return ("Lonely", value * 100)


if __name__ == "__main__":
    pass

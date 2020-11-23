import os
import sys
import argparse
from argparse import RawTextHelpFormatter
from PIL import Image, ImageDraw, ImageFont, ImageOps, UnidentifiedImageError

VERSION = "v0.0.0"


def generate_ogp(ogp_bg, width=1200, height=630, mode="t",
                 overlay_width=1200, overlay_height=300, overlay_opacity=0.75,
                 title_text="", description_text=""):
    """OGP用画像生成

    Args:
        ogp_bg (PIL.Image): OGP背景用画像
        width (int, optional): OGP用画像の横幅 (px). Defaults to 1200.
        height (int, optional): OGP用画像の高さ (px). Defaults to 630.
        mode (str, optional): OGP背景用画像のトリミング位置 (t, c, b). Defaults to "t".
        overlay_width (int, optional): オーバーレイの横幅 (px). Defaults to 1200.
        overlay_height (int, optional): オーバーレイの高さ (px). Defaults to 300.
        overlay_opacity (float, optional): オーバーレイの不透明度 (% / 100). Defaults to 0.75.
        title_text (str, optional): OGP用画像内のタイトル. Defaults to "".
        description_text (str, optional): OGP用画像内の説明. Defaults to "".

    Returns:
        PIL.Image: 生成したOGP用画像
    """
    mode_dict = {
        "t": (0.5, 0.0),  # Top
        "c": (0.5, 0.5),  # Center
        "b": (0.5, 1.0)   # Bottom
    }
    # 指定されたOGP背景用画像をいい感じにトリミング
    canvas = ImageOps.fit(ogp_bg, (width, height), centering=mode_dict[mode]).convert("RGB")
    # オーバーレイの背景を生成
    overlay = Image.new("RGBA", (overlay_width, overlay_height), (0, 0, 0, int(255 * overlay_opacity)))

    if title_text != None and description_text != None:
        draw = ImageDraw.Draw(overlay)

        title_font = ImageFont.truetype("./font/Koruri-Light.ttf", 128)
        description_font = ImageFont.truetype("./font/Koruri-Light.ttf", 48)

        title_font_size = title_font.getsize(title_text)
        description_font_size = description_font.getsize(description_text)

        font_size_width, font_size_height = title_font_size[0] + \
            description_font_size[0], title_font_size[1] + description_font_size[1] - 20

        # タイトル描画
        draw.text((overlay_width // 2 - title_font_size[0] // 2, overlay_height //
                   2 - font_size_height // 2 - description_font_size[1] // 2 - 12), title_text, font=title_font, fill="#FFFFFF")
        # 説明描画
        draw.text((overlay_width // 2 - description_font_size[0] // 2, overlay_height //
                   2 + description_font_size[1] // 2 + 3), description_text, font=description_font, fill="#FFFFFF")

    canvas.paste(overlay, (0, 165), overlay)

    return canvas


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="OGP用画像をいい感じに生成するプログラム by nekocodeX",
                                     epilog="本ソフトウェアは個人用に開発しているものですが、OSSとして公開しています。\nフィードバック等ありましたら、IssueやPull requestを是非送ってください。\n\nGitHub Repo: https://github.com/nekocodeX/OGP-Generator", formatter_class=RawTextHelpFormatter)
    parser.add_argument("-V", "--version",
                        action="version",
                        version=VERSION)
    parser.add_argument("ogp_bg", help="OGP背景用画像のパス", type=str)
    parser.add_argument("-t", "--title", help="OGP用画像内のタイトル", type=str)
    parser.add_argument("-d", "--description", help="OGP用画像内の説明", type=str)
    parser.add_argument("-p", "--position", help="OGP背景用画像のトリミング位置\nt => Top, c => Center, b => Bottom",
                        type=str, choices=["t", "c", "b"], default="t")

    args = parser.parse_args()

    try:
        ogp_bg = Image.open(args.ogp_bg)
    except FileNotFoundError:
        print("[ERROR]", "指定されたOGP背景用画像が見つかりません")
        sys.exit(-1)
    except UnidentifiedImageError:
        print("[ERROR]", "指定されたOGP背景用画像が非対応です")
        sys.exit(-1)

    generate_ogp(ogp_bg, mode=args.position, title_text=args.title, description_text=args.description).save("ogp.png")
    print("[INFO]", "生成完了:", os.path.abspath("./ogp.png"))

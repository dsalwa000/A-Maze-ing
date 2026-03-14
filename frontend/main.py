from mlx import Mlx

# def mymouse(button, x, y, mystuff):
#     print(f"Got mouse event! button {button} at {x},{y}.")

# def mykey(keynum, mystuff):
#     print(f"Got key {keynum}, and got my stuff back:")
#     print(mystuff)
#     if keynum == 32:
#         m.mlx_mouse_hook(win_ptr, None, None)

WALL_COLOR = 4294901760  # red


def my_mlx_pixel_put(img_data: tuple[memoryview, int, int, int], x: int,
                     y: int, color: int):
    addr = img_data[0]
    bits_per_pixel = img_data[1]
    line_length = img_data[2]
    # print(f"line length: {line_length}")
    # print(f"bits per pixel: {bits_per_pixel}")
    offset = int(y * line_length + x * (bits_per_pixel / 8))
    # offset = y * 20 + x
    addr[offset] = color % 256
    addr[offset + 1] = (color >> 8) % 256
    addr[offset + 2] = (color >> 16) % 256
    addr[offset + 3] = (color >> 24) % 256


def has_north(code: int):
    if code % 2:
        return True
    else:
        return False


def has_south(code: int):
    if (code >> 2) % 2:
        return True
    else:
        return False


def has_east(code: int):
    if (code >> 1) % 2:
        return True
    else:
        return False


def has_west(code: int):
    if (code >> 3) % 2:
        return True
    else:
        return False


def draw_wall(data, start, end):
    for x in range(start[0], end[0]):
        for y in range(start[1], end[1]):
            my_mlx_pixel_put(data, x, y, WALL_COLOR)


def draw_cell(data, code: int):
    if has_north(code):
        draw_wall(data, (0, 0), (20, 2))
    if has_south(code):
        draw_wall(data, (0, 18), (20, 20))
    if has_east(code):
        draw_wall(data, (18, 0), (20, 20))
    if has_west(code):
        draw_wall(data, (0, 0), (2, 20))


def init_cell(data):
    for x in range(20):
        for y in range(20):
            my_mlx_pixel_put(data, x, y, 0)


m = Mlx()
mlx_ptr = m.mlx_init()
win_ptr = m.mlx_new_window(mlx_ptr, 500, 500, "Maze")
m.mlx_clear_window(mlx_ptr, win_ptr)

img = m.mlx_new_image(mlx_ptr, 20, 20)
img_data = m.mlx_get_data_addr(img)

code = 9
config = (
    "9515391539551795151151153"
    "EBABAE812853C1412BA812812"
    "96A8416A84545412AC4282C2A"
    "C3A83816A9395384453A82D02"
    "96842A852AC07AAD13A8283C2"
    "C1296C43AAB83AA92AA8686BA"
    "92E853968428444682AC12902"
    "AC3814452FA83FFF82C52C42A"
    "85684117AFC6857FAC1383D06"
    "C53AD043AFFFAFFF856AA8143"
    "91441294297FAFD501142C6BA"
    "AA912AC3843FAFFF82856D52A"
    "842A8692A92B8517C4451552A"
    "816AC384468285293917A9542"
    "C416928513C443A828456C3BA"
    "91416AA92C393A82801553AAA"
    "A81292AA814682C6A8693C6AA"
    "A8442C6C2C1168552C16A9542"
    "86956951692C1455416928552"
    "C545545456C54555545444556"
)
for i in range(len(config)):
    img = m.mlx_new_image(mlx_ptr, 20, 20)
    img_data = m.mlx_get_data_addr(img)
    init_cell(img_data)
    # print(config[i])
    draw_cell(img_data, int(config[i], 16))
    x = (i % 25) * 20
    y = i // 25 * 20
    print(f"for {i}({config[i]}) x: {x}, y: {y}")
    m.mlx_put_image_to_window(mlx_ptr, win_ptr, img, x, y)




# m.mlx_string_put(mlx_ptr, win_ptr, 20, 20, 255, "Hello PyMlx!")
# (ret, w, h) = m.mlx_get_screen_size(mlx_ptr)
# print(f"Got screen size: {w} x {h} .")

# stuff = [1, 2]
# m.mlx_mouse_hook(win_ptr, mymouse, None)
# m.mlx_key_hook(win_ptr, mykey, stuff)

m.mlx_loop(mlx_ptr)

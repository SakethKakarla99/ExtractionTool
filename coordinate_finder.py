import cv2

image = cv2.imread("anthem_page_1.png")


scale = 0.60

display_image = cv2.resize(
    image,
    None,
    fx = scale,
    fy = scale
)

def show_coordinates(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:

        original_x = int(x/scale)
        original_y = int(y/scale)

        print(f"x = {original_x}, y = {original_y}")


cv2.imshow("Authorization Form", display_image)

cv2.setMouseCallback(
    "Authorization Form",
    show_coordinates
)

cv2.waitKey(0)
cv2.destroyAllWindows()
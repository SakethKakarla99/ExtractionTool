import cv2

image = cv2.imread("authorization_form.png")


def show_coordinates(event, x, y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"x = {x}, y = {y}")


cv2.imshow("Authorization Form", image)

cv2.setMouseCallback(
    "Authorization Form",
    show_coordinates
)

cv2.waitKey(0)
cv2.destroyALLWindows()
import cv2
from ultralytics import solutions

cap = cv2.VideoCapture("object_tracking/data/sample_video.mp4")
assert cap.isOpened(), "Error reading video file"

# Video writer
w, h, fps = (int(cap.get(x)) for x in (cv2.CAP_PROP_FRAME_WIDTH, cv2.CAP_PROP_FRAME_HEIGHT, cv2.CAP_PROP_FPS))
video_writer = cv2.VideoWriter("object_counting_output.avi", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

region_points = [(0, int(h/2)), (int(w), int(h/2))] # line counting

# Initialize object counter object
counter = solutions.ObjectCounter(
    show = True,  # display the output (False olunca ek pencere açmaz)
    region = region_points,  # pass region points
    model = "yolo11n.pt",  # model="yolo11n-obb.pt" for object counting with OBB model.
    classes = [2, 5, 7],  # count specific classes i.e. person and car with COCO pretrained model.
    tracker ="botsort.yaml",  # choose trackers i.e "bytetrack.yaml"
    device = 0,
    conf = 0.5,
    line_width = 2,
    half = True,
    show_in = True,
    show_out = True,
    analytics_type="line"
)

# Process video
while cap.isOpened():
    success, im0 = cap.read()

    if not success:
        print("Video frame is empty or processing is complete.")
        break

    results = counter(im0)  # işlem sonucu

    frame = results.plot_im  # YOLO çizimleri yapılmış kare

    video_writer.write(frame)  # tek dosyaya yazdır

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
video_writer.release()
cv2.destroyAllWindows()  # destroy all opened windows
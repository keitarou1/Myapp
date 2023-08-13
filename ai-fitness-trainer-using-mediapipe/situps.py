import cv2
import mediapipe as mp



class SitupsCounter:
    def __init__(self, mode=False, complexity=1, smooth_landmarks=True,
                    enable_segmentation=False, smooth_segmentation=True,
                    detectionCon=0.5, trackCon=0.5):
        self.mode = mode 
        self.complexity = complexity
        self.smooth_landmarks = smooth_landmarks
        self.enable_segmentation = enable_segmentation
        self.smooth_segmentation = smooth_segmentation
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(self.mode, self.complexity, self.smooth_landmarks,
                                     self.enable_segmentation, self.smooth_segmentation,
                                     self.detectionCon, self.trackCon,)
        self.situp_count = 0
        self.is_up = False

    def detect_situp(self, landmarks):
        left_shoulder = landmarks[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y
        left_hip = landmarks[self.mp_pose.PoseLandmark.LEFT_HIP.value].y
        right_shoulder = landmarks[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y
        right_hip = landmarks[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y
        
        if left_shoulder < left_hip and right_shoulder < right_hip:
            self.is_up = True
        elif left_shoulder > left_hip and right_shoulder > right_hip and self.is_up:
            self.situp_count += 1
            self.is_up = False

def main():
    global run
    situps_counter = SitupsCounter()
    co =0
    cap = cv2.VideoCapture(0)  # Open the default camera

    while cap.isOpened:
                ret, frame = cap.read()
                width  = cap.get(3)  # float `width`
                height = cap.get(4) 

                results = situps_counter.pose.process(frame)

                if results.pose_landmarks:
                    situps_counter.detect_situp(results.pose_landmarks.landmark)
                    situp_count = situps_counter.situp_count

                    cv2.putText(frame, f"Sit-ups: {situp_count}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    situps_counter.mp_drawing.draw_landmarks(frame, results.pose_landmarks, situps_counter.mp_pose.POSE_CONNECTIONS)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()

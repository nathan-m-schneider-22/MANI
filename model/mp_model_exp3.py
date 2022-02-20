import cv2
import mediapipe as mp
import numpy as np
from typing import List

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


# embed landmarks into feature vector
class HandModel(object):
    """
    Params
        landmarks: List of positions
    Args
        connections: List of tuples containing the ids of the two landmarks representing a connection
        feature_vector: List of length 21 * 21 = 441 containing the angles between all connections
    """

    def __init__(self, landmarks: List[float]):

        # Define the connections
        self.connections = mp.solutions.holistic.HAND_CONNECTIONS

        # Create feature vector (list of the angles between all the connections)
        landmarks = self.construct_landmarks(landmarks)
        self.feature_vector = self._get_feature_vector(landmarks)
    
    def construct_landmarks(self, hlandmarks):
        landmarks = np.ones((21, 3))
        for idx, lm in enumerate(hlandmarks):
            landmarks[idx,:] = [lm.x, lm.y, lm.z]
        return landmarks

    def _get_feature_vector(self, landmarks: np.ndarray) -> List[float]:
        """
        Params
            landmarks: numpy array of shape (21, 3)
        Return
            List of length nb_connections * nb_connections containing
            all the angles between the connections
        """
        connections = self._get_connections_from_landmarks(landmarks)

        angles_list = []
        for connection_from in connections:
            for connection_to in connections:
                angle = self._get_angle_between_vectors(connection_from, connection_to)
                # If the angle is not NaN we store it else we store 0
                if angle == angle:
                    angles_list.append(angle)
                else:
                    angles_list.append(0)
        return angles_list

    def _get_connections_from_landmarks(
        self, landmarks: np.ndarray
    ) -> List[np.ndarray]:
        """
        Params
            landmarks: numpy array of shape (21, 3)
        Return
            List of vectors representing hand connections
        """
        return list(
            map(
                lambda t: landmarks[t[1]] - landmarks[t[0]],
                self.connections,
            )
        )

    @staticmethod
    def _get_angle_between_vectors(u: np.ndarray, v: np.ndarray) -> float:
        """
        Args
            u, v: 3D vectors representing two connections
        Return
            Angle between the two vectors
        """
        if np.array_equal(u, v):
            return 0
        dot_product = np.dot(u, v)
        norm = np.linalg.norm(u) * np.linalg.norm(v)
        return np.arccos(dot_product / norm)


# For static images:
IMAGE_FILES = ["../data/a/a2.jpg"]
with mp_hands.Hands(
    static_image_mode=True,
    max_num_hands=1,
    min_detection_confidence=0) as hands:
  for idx, file in enumerate(IMAGE_FILES):
    # Read an image, flip it around y-axis for correct handedness output (see
    # above).
    image = cv2.flip(cv2.imread(file), 1)
    # Convert the BGR image to RGB before processing.
    results = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    # Print handedness and draw hand landmarks on the image.
    print('Handedness:', results.multi_handedness)
    if not results.multi_hand_landmarks:
      print("heree")
      continue
    image_height, image_width, _ = image.shape
    annotated_image = image.copy()
    for hand_landmarks in results.multi_hand_landmarks:
      print(hand_landmarks.landmark)
      hm = HandModel(hand_landmarks.landmark)
    
      print(len(hm.feature_vector))
      print('hand_landmarks:', hand_landmarks)
      print(
          f'Index finger tip coordinates: (',
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image_width}, '
          f'{hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image_height})'
      )
      mp_drawing.draw_landmarks(
          annotated_image,
          hand_landmarks,
          mp_hands.HAND_CONNECTIONS,
          mp_drawing_styles.get_default_hand_landmarks_style(),
          mp_drawing_styles.get_default_hand_connections_style())
    cv2.imwrite(
        '/tmp/annotated_image' + str(idx) + '.png', cv2.flip(annotated_image, 1))
    # Draw hand world landmarks.
    if not results.multi_hand_world_landmarks:
      continue
    for hand_world_landmarks in results.multi_hand_world_landmarks:
      mp_drawing.plot_landmarks(
        hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)



import cv2


def create_default_kalman():
    kalman = cv2.cv.CreateKalman(4, 2, 0)

    kalman.transition_matrix[0, 0] = 1
    kalman.transition_matrix[1, 1] = 1
    kalman.transition_matrix[2, 2] = 1
    kalman.transition_matrix[3, 3] = 1
    kalman.transition_matrix[0, 2] = 1
    kalman.transition_matrix[1, 3] = 1

    kalman.state_pre[0, 0] = 0
    kalman.state_pre[1, 0] = 0
    kalman.state_pre[2, 0] = 0
    kalman.state_pre[3, 0] = 0

    cv2.cv.SetIdentity(kalman.measurement_matrix, cv2.cv.RealScalar(1))
    cv2.cv.SetIdentity(kalman.process_noise_cov, cv2.cv.RealScalar(1e-5)) # 1e-5
    cv2.cv.SetIdentity(kalman.measurement_noise_cov, cv2.cv.RealScalar(1e-1))
    cv2.cv.SetIdentity(kalman.error_cov_post, cv2.cv.RealScalar(0.1))

    cv2.cv.KalmanPredict(kalman)

    return kalman
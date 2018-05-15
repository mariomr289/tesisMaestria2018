import numpy
import cv2


def main():

    camaraWeb()

    #cargarVideo()

    guardarVideo()


    return

def camaraWeb():

    cap = cv2.VideoCapture(0)

    while(True):
        # Captura frame por frame
        ret,frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


        cv2.imshow('frame',frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


def cargarVideo():

    cap = cv2.VideoCapture("videos/saludo.avi")

    while(cap.isOpened()):

        ret, frame = cap.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        cv2.imshow('frame',gray)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def guardarVideo():

    cap = cv2.VideoCapture(0)

    # Definimos el codec a usar
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    out = cv2.VideoWriter('videos/output.avi',fourcc, 20.0, (640,480))

    while(cap.isOpened()):

        ret, frame = cap.read()
        if ret==True:
            #frame = cv2.flip(frame,0)


            out.write(frame)


            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    # Cerramos la conexion
    cap.release()
    out.release()
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()

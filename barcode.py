import cv2
from pyzbar.pyzbar import decode

# Webcam'i açın
cap = cv2.VideoCapture(0)

# Barkodu takip etmek için değişkenler
tracked_barcode_data = None
track = False

while True:
    # Kameradan bir çerçeve alın
    _, frame = cap.read()

    # Barkodları tara
    barcodes = decode(frame)

    # Barkodları bulun ve çerçeve üzerine yazın
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeType = barcode.type
        
        if track and barcode.data.decode("utf-8") == tracked_barcode_data:
            # Takip edilen barkodu işaretle
            text = "{} ({})".format(tracked_barcode_data, barcodeType)
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
            #cv2.rectangle(frame, barcode.rect, (0, 255, 0), 2)
        else:
            # Yeni bir barkodu takip etmeye başlayın
            tracked_barcode_data = barcode.data.decode("utf-8")
            tracking = True
            print("Barkod girdi: {}".format(tracked_barcode_data))
            
    # Eğer hiç barkod bulunmuyorsa takip durumunu sıfırlayın
    if not barcodes and track:
        tracking = False
        print("Barkod çıktı: {}".format(tracked_barcode_data))

    cv2.imshow("Webcam", frame)

    # 'q' tuşuyla kapa
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

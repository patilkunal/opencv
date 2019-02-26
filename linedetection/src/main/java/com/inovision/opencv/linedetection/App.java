package com.inovision.opencv.linedetection;

import java.awt.Image;
import java.awt.image.BufferedImage;
import java.awt.image.DataBufferByte;
import java.awt.image.WritableRaster;

import org.opencv.core.Core;
import org.opencv.core.CvType;
import org.opencv.core.Mat;
import org.opencv.core.Scalar;

/**
 * Hello world!
 *
 */
public class App {
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);		
	}
    public static void main( String[] args ) {
        
        Mat mat = Mat.eye(3,3, CvType.CV_8UC1);
        System.out.println("mat = " + mat.dump());
        
        System.out.println("Welcome to OpenCV " + Core.VERSION);
        Mat m = new Mat(5, 10, CvType.CV_8UC1, new Scalar(0));
        System.out.println("OpenCV Mat: " + m);
        Mat mr1 = m.row(1);
        mr1.setTo(new Scalar(1));
        Mat mc5 = m.col(5);
        mc5.setTo(new Scalar(5));
        System.out.println("OpenCV Mat data:\n" + m.dump());
        
    }
    
    public Image toBufferedImage(Mat m) {
        int type = BufferedImage.TYPE_BYTE_GRAY;
        if ( m.channels() > 1 ) {
            type = BufferedImage.TYPE_3BYTE_BGR;
        }
        int bufferSize = m.channels()*m.cols()*m.rows();
        byte [] b = new byte[bufferSize];
        m.get(0,0,b); // get all the pixels
        BufferedImage image = new BufferedImage(m.cols(),m.rows(), type);
        final byte[] targetPixels = ((DataBufferByte) image.getRaster().getDataBuffer()).getData();
        System.arraycopy(b, 0, targetPixels, 0, b.length);  
        return image;

    }
    
    /*
    public void matToBuffereddImage() {
    	Mat m = HighGui. imread("some.png");
    	int type = BufferedImage.TYPE_BYTE_GRAY;
    	if ( m.channels() > 1 ) {
    	    Mat m2 = new Mat();
    	    Imgproc.cvtColor(m,m2,Imgproc.COLOR_BGR2RGB);
    	    type = BufferedImage.TYPE_3BYTE_BGR;
    	    m = m2;
    	}
    	byte [] b = new byte[m.channels()*m.cols()*m.rows()];
    	m.get(0,0,b); // get all the pixels
    	BufferedImage image = new BufferedImage(m.cols(),m.rows(), type);
    	image.getRaster().setDataElements(0, 0, m.cols(),m.rows(), b);  

    	// later:
    	//public synchronized void update(Graphics g)
    	//{
    	//    g.drawImage(image,0,0,this);    
    	//}
    }
    
    */
    
    /**
     * Converts/writes a Mat into a BufferedImage.
     * 
     * @param matrix Mat of type CV_8UC3 or CV_8UC1
     * @return BufferedImage of type TYPE_3BYTE_BGR or TYPE_BYTE_GRAY
     */
    public static BufferedImage matToBufferedImage(Mat matrix) {
        int cols = matrix.cols();
        int rows = matrix.rows();
        int elemSize = (int)matrix.elemSize();
        byte[] data = new byte[cols * rows * elemSize];
        int type;

        matrix.get(0, 0, data);

        switch (matrix.channels()) {
            case 1:
                type = BufferedImage.TYPE_BYTE_GRAY;
                break;

            case 3: 
                type = BufferedImage.TYPE_3BYTE_BGR;

                // bgr to rgb
                byte b;
                for(int i=0; i<data.length; i=i+3) {
                    b = data[i];
                    data[i] = data[i+2];
                    data[i+2] = b;
                }
                break;

            default:
                return null;
        }

        BufferedImage image = new BufferedImage(cols, rows, type);
        image.getRaster().setDataElements(0, 0, cols, rows, data);

        return image;
    }
    
    /*
    public void imshow(Mat src){
        BufferedImage bufImage = null;
        try {
            MatOfByte matOfByte = new MatOfByte();
            Highgui.imencode(".jpg", src, matOfByte); 
            byte[] byteArray = matOfByte.toArray();
            InputStream in = new ByteArrayInputStream(byteArray);
            bufImage = ImageIO.read(in);

            JFrame frame = new JFrame("Image");
            frame.getContentPane().setLayout(new FlowLayout());
            frame.getContentPane().add(new JLabel(new ImageIcon(bufImage)));
            frame.pack();
            frame.setVisible(true);
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    */
}

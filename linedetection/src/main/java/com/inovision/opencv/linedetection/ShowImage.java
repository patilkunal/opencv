package com.inovision.opencv.linedetection;

import org.opencv.core.Core;
import org.opencv.core.Mat;
import org.opencv.imgcodecs.Imgcodecs;

import com.inovision.opencv.filter.GreenFilter;

public class ShowImage {
	
	static {
		System.loadLibrary(Core.NATIVE_LIBRARY_NAME);
	}

	public static void main(String args[]) {
		String path = "/temp/parking.png";
		Mat image = Imgcodecs.imread(path);
		if(image.dataAddr() == 0) {
			System.out.println("Unable to load image " + path);
		} else {
			ImageViewer viewer = new ImageViewer();
			viewer.show(image, "Original");
			
			viewer = new ImageViewer(new GreenFilter());
			viewer.show(image, "Filtered");
		}
	}
}

package com.inovision.opencv.linedetection;

import java.awt.Graphics;
import java.awt.Panel;
import java.awt.image.BufferedImage;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;

import javax.imageio.ImageIO;
import javax.swing.JFrame;

public class ShowImageSwing extends Panel {
	BufferedImage image;

	public ShowImageSwing() {
		try {
			System.out.println("Enter image name\n");
			BufferedReader bf = new BufferedReader(new InputStreamReader(System.in));
			String imageName = bf.readLine();
			File input = new File(imageName);
			image = ImageIO.read(input);
		} catch (IOException ie) {
			System.out.println("Error:" + ie.getMessage());
		}
	}

	public void paint(Graphics g) {
		g.drawImage(image, 0, 0, null);
	}

	static public void main(String args[]) throws Exception {
		JFrame frame = new JFrame("Display image");
		Panel panel = new ShowImageSwing();
		frame.getContentPane().add(panel);
		frame.setSize(500, 500);
		frame.setVisible(true);
	}
}
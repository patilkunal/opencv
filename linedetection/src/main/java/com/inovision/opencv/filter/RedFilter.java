package com.inovision.opencv.filter;

public class RedFilter implements Filter {

	@Override
	public void apply(byte[] buffer) {
		for (int i = 0; i < buffer.length; i++) {
			if (i % 3 == 1)
				buffer[i] = 0;
		}
	}

}

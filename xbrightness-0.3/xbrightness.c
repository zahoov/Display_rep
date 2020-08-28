/*
 * Copyright 2003 Asher Blum <asher@wildspark.com>
 *
 * Permission is hereby granted, free of charge, to any person obtaining a
 * copy of this software and associated documentation files (the "Software"),
 * to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense,
 * and/or sell copies of the Software, and to permit persons to whom the
 * Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
 * THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
 * WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF
 * OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 *
 * Written by Asher Blum <asher@wildspark.com>
 */

#include <ctype.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <X11/Xos.h>
#include <X11/Xlib.h>
#include <X11/Xutil.h>
#include <X11/extensions/xf86vmode.h>
#include <math.h>

char *argv0;

static void syntax(void) {
    fprintf (stderr, "%s builds a brightness ramp for X11.\n\n", argv0);
    fprintf (stderr, "usage:  %s BRIGHTNESS [ GBASE ]\n\n", argv0);
    fprintf (stderr, "where BRIGHTNESS is a number from 0 to 65535.\n");
    fprintf (stderr, "where GBASE is a float number from 0.0 to 10.0. (default=1.0)\n");
    exit (1);
}

int main(int argc, char *argv[]) {
    int i;
    Display *dpy;
    int screen = -1;
    int ramp_size = 0;
    unsigned short *ramp;
    unsigned short brightness = 60000;
    float k;
    double gbase = 1.0;

    /**** Read arguments ****/

    argv0 = argv[0];

    if((argc != 2) && (argc !=3)){
        syntax();
    }

    i = atoi(argv[1]);
    if(!i && (argv[1][1] || !isdigit(argv[1][0]))) {
        syntax();
    }
    if(i<0 || i>65535) {
        syntax();
    }
    brightness=i;

    if (argc == 3) {
	gbase = atof (argv[2]);
	if (gbase == 0.0) {
	    syntax();
	}
    }
    
    /**** Setup ****/

    if ((dpy = XOpenDisplay(NULL)) == NULL) {
        fprintf (stderr, "%s:  unable to open default display.\n",
        argv0);
        exit(1);
    }

    screen = DefaultScreen(dpy);

    /**** main portion ****/

    if (!XF86VidModeGetGammaRampSize(dpy, screen, &ramp_size)) {
        fprintf(stderr, "Unable to query gamma ramp size\n");
        XCloseDisplay (dpy);
        exit (2);
    }
    
    ramp = (unsigned short *) malloc (ramp_size * sizeof(unsigned short));
    if (ramp == NULL) {
	fprintf(stderr, "could not allocate %lu bytes, aborting\n", (unsigned long)(ramp_size * sizeof(unsigned short)));
	XCloseDisplay (dpy);
	exit (2);
    }

    if (!XF86VidModeGetGammaRamp(dpy, screen, ramp_size, ramp, ramp, ramp)) {
        fprintf(stderr, "Unable to query brightness\n");
        XCloseDisplay (dpy);
        exit (2);
    }

    for(i=0; i<ramp_size; i++) {
	double p = ((double) i)/ramp_size;
        ramp[i] = (unsigned short)(brightness * pow (p, gbase));
    }

    if(!XF86VidModeSetGammaRamp(dpy, screen, ramp_size, ramp, ramp, ramp)) {
        fprintf(stderr, "Unable to set brightness");
        XCloseDisplay (dpy);
        exit (2);
    }

    XCloseDisplay (dpy);
    exit (0);
}


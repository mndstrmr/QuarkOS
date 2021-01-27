#include <syscall.h>
#include <stdio.h>
#include <assertions.h>
#include <string.h>

#include "themes/theme.h"
#include "input.h"
#include "request.h"
#include "render.h"
#include "buffer.h"

char rawrequest[1024];
void recieve_messages() {
	unsigned sender;

	while (1) {
		update_cursor();
		update_keyboard();
		
		int status = read_ipc_message(rawrequest, 1024, &sender);
		while (status >= 0) {
			WindowServerAction action = ((WindowServerRequest*) rawrequest)->action;
			handle_request(action, sender, rawrequest);
			memset(rawrequest, 0, 1024);

			status = read_ipc_message(rawrequest, 1024, &sender);
		}
		
		render();
	}
}

int main() {
	initialise_buffers();
	initialise_mouse();
	initialise_keyboard();

#if ACTIVE_THEME_GRAY
	set_theme(create_gray_theme());
#else
	set_theme(create_hacker_theme());
#endif
	
	render();

	exec("/usr/bin/dock");

	recieve_messages();

	return 0;
}

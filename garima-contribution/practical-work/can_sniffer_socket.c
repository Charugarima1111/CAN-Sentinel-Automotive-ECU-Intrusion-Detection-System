
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <linux/can.h>
#include <linux/can/raw.h>

#define SOCKET_PATH "/tmp/can_sentinel.sock"

int main(void)
{
    int can_sock, unix_sock;
    struct sockaddr_can can_addr;
    struct sockaddr_un unix_addr;
    struct ifreq ifr;
    struct can_frame frame;
    char message[128];

    /* Connect to the Python Unix Domain Socket server */
    unix_sock = socket(AF_UNIX, SOCK_STREAM, 0);
    if (unix_sock < 0) {
        perror("Unix socket");
        return 1;
    }

    memset(&unix_addr, 0, sizeof(unix_addr));
    unix_addr.sun_family = AF_UNIX;
    strncpy(unix_addr.sun_path, SOCKET_PATH,
            sizeof(unix_addr.sun_path) - 1);

    printf("Waiting for Python receiver...\n");

    if (connect(unix_sock, (struct sockaddr *)&unix_addr,
                sizeof(unix_addr)) < 0) {
        perror("Connect to Python receiver");
        close(unix_sock);
        return 1;
    }

    /* Open the CAN interface */
    can_sock = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    if (can_sock < 0) {
        perror("CAN socket");
        close(unix_sock);
        return 1;
    }

    memset(&ifr, 0, sizeof(ifr));
    strcpy(ifr.ifr_name, "vcan0");

    if (ioctl(can_sock, SIOCGIFINDEX, &ifr) < 0) {
        perror("Interface lookup");
        close(can_sock);
        close(unix_sock);
        return 1;
    }

    memset(&can_addr, 0, sizeof(can_addr));
    can_addr.can_family = AF_CAN;
    can_addr.can_ifindex = ifr.ifr_ifindex;

    if (bind(can_sock, (struct sockaddr *)&can_addr,
             sizeof(can_addr)) < 0) {
        perror("CAN bind");
        close(can_sock);
        close(unix_sock);
        return 1;
    }

    printf("CAN-Sentinel C-to-Python integration started.\n");
    printf("Monitoring vcan0.\n");
    printf("Press Ctrl+C to stop.\n\n");

    while (1) {
        int nbytes = read(can_sock, &frame, sizeof(frame));

        if (nbytes < 0) {
            if (errno == EINTR)
                continue;
            perror("CAN read");
            break;
        }

        if (nbytes != sizeof(frame)) {
            fprintf(stderr, "Incomplete CAN frame\n");
            continue;
        }

        int offset = snprintf(
            message, sizeof(message),
            "%03X,%u,",
            frame.can_id & CAN_EFF_MASK,
            frame.len
        );

        for (int i = 0; i < frame.len; i++) {
            offset += snprintf(
                message + offset,
                sizeof(message) - offset,
                "%02X",
                frame.data[i]
            );
        }

        message[offset++] = '\n';

        if (write(unix_sock, message, offset) != offset) {
            perror("Send to Python");
            break;
        }

        printf("Forwarded CAN ID: 0x%03X to Python\n",
               frame.can_id & CAN_EFF_MASK);
        fflush(stdout);
    }

    close(can_sock);
    close(unix_sock);
    return 0;
}


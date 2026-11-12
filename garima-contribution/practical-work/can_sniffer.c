
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <errno.h>
#include <net/if.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <linux/can.h>
#include <linux/can/raw.h>

int main(void)
{
    int sock;
    struct sockaddr_can addr;
    struct ifreq ifr;
    struct can_frame frame;

    sock = socket(PF_CAN, SOCK_RAW, CAN_RAW);
    if (sock < 0) {
        perror("CAN socket");
        return 1;
    }

    memset(&ifr, 0, sizeof(ifr));
    strcpy(ifr.ifr_name, "vcan0");

    if (ioctl(sock, SIOCGIFINDEX, &ifr) < 0) {
        perror("Interface lookup");
        close(sock);
        return 1;
    }

    memset(&addr, 0, sizeof(addr));
    addr.can_family = AF_CAN;
    addr.can_ifindex = ifr.ifr_ifindex;

    if (bind(sock, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("CAN bind");
        close(sock);
        return 1;
    }

    printf("CAN-Sentinel C Sniffer Started\n");
    printf("Monitoring interface: vcan0\n");
    printf("Press Ctrl+C to stop.\n\n");

    while (1) {
        int nbytes = read(sock, &frame, sizeof(frame));

        if (nbytes < 0) {
            perror("CAN read");
            break;
        }

        if (nbytes != sizeof(frame)) {
            fprintf(stderr, "Incomplete CAN frame received\n");
            continue;
        }

        printf("CAN ID: 0x%03X | DLC: %d | Data: ",
               frame.can_id & CAN_EFF_MASK,
               frame.len);

        for (int i = 0; i < frame.len; i++) {
            printf("%02X ", frame.data[i]);
        }

        printf("\n");
        fflush(stdout);
    }

    close(sock);
    return 0;
}


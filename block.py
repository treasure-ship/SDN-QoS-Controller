from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet import ethernet, ipv4, arp
from pox.lib.addresses import IPAddr, EthAddr

log = core.getLogger()

BLOCKED_SRC = "10.0.0.1"
BLOCKED_DST = "10.0.0.2"

class LearningSwitch(object):
    """
    A proper learning switch that:
    - Learns which MAC is on which port
    - Blocks h1 -> h2 only
    - Forwards everything else correctly
    """

    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}   # stores: MAC address -> port number
        connection.addListeners(self)
        log.info("Switch connected - QoS Controller ready")
        log.info("Rule: %s -> %s is BLOCKED", BLOCKED_SRC, BLOCKED_DST)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        if not packet.parsed:
            return

        in_port = event.port

        # LEARN: save which port this MAC address came from
        src_mac = packet.src
        self.mac_to_port[src_mac] = in_port
        log.debug("Learned: MAC %s is on port %s", src_mac, in_port)

        # CHECK IF IP PACKET and should be blocked
        if packet.type == ethernet.IP_TYPE:
            ip_pkt = packet.find('ipv4')
            if ip_pkt:
                src_ip = str(ip_pkt.srcip)
                dst_ip = str(ip_pkt.dstip)
                log.info("IP: %s -> %s", src_ip, dst_ip)

                # BLOCK h1 -> h2 only
                if src_ip == BLOCKED_SRC and dst_ip == BLOCKED_DST:
                    log.info("*** BLOCKED: %s -> %s ***", src_ip, dst_ip)
                    self._install_drop_rule(src_ip, dst_ip)
                    return  # drop current packet too

        # FOR EVERYTHING ELSE: forward smartly using learned MACs
        dst_mac = packet.dst

        if dst_mac in self.mac_to_port:
            # We know which port to send to - send directly
            out_port = self.mac_to_port[dst_mac]
            log.info("Forwarding to known port %s", out_port)
            self._send_packet(event, out_port)
        else:
            # We don't know - flood to all ports
            log.info("Unknown destination - flooding")
            self._send_packet(event, of.OFPP_FLOOD)

    def _install_drop_rule(self, src_ip, dst_ip):
        """Install permanent drop rule for h1->h2"""
        msg = of.ofp_flow_mod()
        msg.match.dl_type = 0x0800
        msg.match.nw_src = IPAddr(src_ip)
        msg.match.nw_dst = IPAddr(dst_ip)
        msg.priority = 200
        msg.idle_timeout = 0
        msg.hard_timeout = 0
        # No actions = drop
        self.connection.send(msg)
        log.info("Drop rule installed: %s -> %s", src_ip, dst_ip)

    def _send_packet(self, event, out_port):
        """Send packet out a specific port"""
        msg = of.ofp_packet_out()
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.data = event.ofp
        msg.in_port = event.port
        self.connection.send(msg)


class QoSLauncher(object):
    def __init__(self):
        core.openflow.addListenerByName(
            "ConnectionUp",
            self._handle_ConnectionUp
        )

    def _handle_ConnectionUp(self, event):
        LearningSwitch(event.connection)


def launch():
    log.info("QoS Priority Controller starting...")
    QoSLauncher()

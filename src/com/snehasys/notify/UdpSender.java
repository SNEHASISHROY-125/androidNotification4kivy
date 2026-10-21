
package com.snehasys.notify;

// import android.util.Log;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;

public class UdpSender {
    // private static final String TAG = "UdpSender";
    private static String SERVER_IP = "127.0.0.1"; // or your host machine IP on LAN
    private static int SERVER_PORT = 28976;

    
    // ----------- OSC Send Helper -----------

    public static void sendOsc(String address, Object... args) {
        new Thread(() -> {
            try (DatagramSocket socket = new DatagramSocket()) {
                InetAddress addr = InetAddress.getByName(SERVER_IP);

                ByteBuffer buf = ByteBuffer.allocate(512);
                // Force buffer to be big-endian (OSC standard)
                buf.order(java.nio.ByteOrder.BIG_ENDIAN);

                // Write address
                buf.put(oscPad(address));

                // Write type tags
                StringBuilder tags = new StringBuilder(",");
                for (Object arg : args) {
                    if (arg instanceof Integer) tags.append("i");
                    else if (arg instanceof Float) tags.append("f");
                    else if (arg instanceof Boolean) tags.append((Boolean) arg ? "T" : "F");
                    else tags.append("s");
                }
                buf.put(oscPad(tags.toString()));

                // Write arguments
                for (Object arg : args) {
                    if (arg instanceof Integer) {buf.putInt((Integer) arg);}
                    else if (arg instanceof Float) {buf.putFloat((Float) arg);}
                    else if (arg instanceof Boolean) {
                        // NO DATA for boolean in OSC
                    }
                    else {buf.put(oscPad(String.valueOf(arg)));}
                }

                byte[] data = new byte[buf.position()];
                buf.flip();
                buf.get(data);

                DatagramPacket packet = new DatagramPacket(data, data.length, addr, SERVER_PORT);
                socket.send(packet);

                System.out.println("Sent OSC: " + address);

            } catch (Exception e) {
                System.err.println("Failed to send OSC: " + e);
            }
        }).start();
    }

    // private static byte[] oscPad(String s) {
    //     byte[] strBytes = s.getBytes(StandardCharsets.UTF_8);
    //     int pad = 4 - (strBytes.length % 4);
    //     if (pad == 4) pad = 0;
    //     ByteBuffer buf = ByteBuffer.allocate(strBytes.length + pad);
    //     buf.put(strBytes);
    //     for (int i = 0; i < pad; i++) buf.put((byte) 0);
    //     return buf.array();
    // }

        private static byte[] oscPad(String s) {
        byte[] strBytes = s.getBytes(StandardCharsets.UTF_8);

        int len = strBytes.length + 1; // include null terminator
        int pad = (4 - (len % 4)) % 4;

        ByteBuffer buf = ByteBuffer.allocate(len + pad);
        buf.put(strBytes);
        buf.put((byte) 0); // null terminator

        for (int i = 0; i < pad; i++) {
            buf.put((byte) 0);
        }

        return buf.array();
    }

}

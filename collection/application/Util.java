package research;

import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.text.SimpleDateFormat;
import java.util.Date;

/*
Create an object of this class to validate your solutions for the computational race GVS challenge.
 */
public class Util {

    private static final SimpleDateFormat format = new SimpleDateFormat("dd.MM.yyyy hh:mm:ss");

    public static String time(){
        return format.format(new Date());
    }

    public static void log(String s) { System.out.println(System.nanoTime()+": "+s); }
    public static void log_pretty(String s) { System.out.println(time()+": "+s); }

    /*
    Use this function to convert bytes to a String
     */
    public static String bytesToHex(byte[] in) {
        final StringBuilder builder = new StringBuilder();
        for (byte b : in) {
            builder.append(String.format("%02x", b));
        }
        return builder.toString();
    }

    private MessageDigest md;

    public Util() throws java.security.NoSuchAlgorithmException {
        this.md = MessageDigest.getInstance("SHA-256");
    }

    public String hash(String data) {
        md.update(data.getBytes(StandardCharsets.UTF_8));
        return bytesToHex(md.digest());
    }
}
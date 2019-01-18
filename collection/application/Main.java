package research;

import org.bitcoinj.core.NetworkParameters;
import org.bitcoinj.core.PeerGroup;
import org.bitcoinj.net.discovery.DnsDiscovery;
import org.bitcoinj.params.MainNetParams;
import org.bitcoinj.utils.BriefLogFormatter;

import java.io.IOException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Main {

    public static void main(String[] args) throws IOException {
        BriefLogFormatter.init();

        NetworkParameters params = MainNetParams.get();

        // Setup PeersGroup of Bitcoinj to connect to many nodes etc.
        PeerGroup peers = new PeerGroup(params);
        peers.setMaxConnections(5000);
        peers.setMinBroadcastConnections(100000);
        peers.setUserAgent("UU-Network-Research", "0.1");
        peers.addPeerDiscovery(new DnsDiscovery(params));

        Util.log_pretty("Starting Crawler.");
        Util.log_pretty("Max allowed connections: "+peers.getMaxConnections());
        Util.log_pretty("Min broadcast connections: "+peers.getMinBroadcastConnections());

        // Start up the peers, so they will form connections
        peers.start();

        // Status reprorting thread
        ExecutorService pool = Executors.newSingleThreadExecutor();
        pool.execute(()->{
            try {
            while(!Thread.currentThread().isInterrupted()){
                System.out.print("\r"+Util.time()+" Peers: "+peers.getConnectedPeers().size());

                Thread.sleep(334);
            }
            } catch (InterruptedException e) {}
        });

        // Wait for keyboard input to shutdown
        System.in.read();
        Util.log_pretty("Shutdown");
        pool.shutdownNow();
    }
}


package com.bionet;

import org.apache.camel.main.Main;

public class BionetApp {
    public static void main(String[] args) throws Exception {
        Main main = new Main();
        main.configure().addRoutesBuilder(new FileTransferRoute());
        main.run();
    }
}

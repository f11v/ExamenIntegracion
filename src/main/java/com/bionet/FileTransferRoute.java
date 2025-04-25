
package com.bionet;

import org.apache.camel.builder.RouteBuilder;

public class FileTransferRoute extends RouteBuilder {
    @Override
    public void configure() throws Exception {
        from("file:input-labs?noop=true&readLock=changed")
            .choice()
                .when(header("CamelFileName").endsWith(".csv"))
                    .to("file:processed")
                .otherwise()
                    .to("file:error");
    }
}

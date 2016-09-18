
/**
 * @author paridhika
 *
 */
package com.acme.callbacks;
import java.nio.charset.StandardCharsets;

import com.hivemq.spi.callback.CallbackPriority;
import com.hivemq.spi.callback.events.OnSubscribeCallback;
import com.hivemq.spi.callback.exception.InvalidSubscriptionException;
import com.hivemq.spi.message.SUBSCRIBE;
import com.hivemq.spi.message.PUBLISH;
import com.hivemq.spi.message.QoS;
import com.hivemq.spi.services.PublishService; 
import com.hivemq.spi.security.ClientData;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.google.inject.Inject;
import com.acme.configuration.Configuration;

public class SubscribeReceived implements OnSubscribeCallback {

	final Logger logger = LoggerFactory.getLogger(SubscribeReceived.class);
	
	private PublishService publishService;
	
	@Override
	public void onSubscribe(final SUBSCRIBE message, final ClientData clientData) throws InvalidSubscriptionException {
		logger.info("Client {} is now subscribed to the topics: {}.", clientData.getClientId(), message.getTopics());
		PUBLISH msg = new PUBLISH();
		String location = Configuration.findLocation();
		msg.setQoS(QoS.EXACTLY_ONCE);
		msg.setTopic("loc/get");	
		msg.setPayload(location.getBytes());
		msg.setRetain(true);
		this.publishService.publish(msg);
	}
	
	@Inject
    public SubscribeReceived(final PublishService publishService) {
        this.publishService = publishService;
    }


	@Override
	public int priority() {
		return CallbackPriority.MEDIUM;
	}
}

"""
testdriver.py is a collection of functions in order to test the
behavior of Redis, deployed in an HA environment inside a Docker
Datacenter Cluster.

"""
__author__ = "Chris King"
__email__ = "chris.king@kilncode.com"
__owner__ = "MetLife"


# Global Imports
import redis
from fabric.api import * 
import unittest
import time


# Global Connection Information
env.user = "root"
REDIS_PORT =  6379
SWARM_NODE_1 = "169.46.44.168"
SWARM_NODE_2 = "169.46.44.189"
SWARM_NODE_3 = "169.46.44.167"

# Test Scenarios
class RedisTest(unittest.TestCase):

    def setUp(self):
        """
        Here we need to establish a connection to the Redis cluster.
        This is actually a HAProxy node that is proxying our traffic. 

        So connecting here actually validates the following:
        1. HAProxy forwarding to a Redis Master instance.
        2. Redis cluster is up.
        3. Networkign connectivity is good.
        """
        self.redis = redis.Redis(host=SWARM_NODE_1, port=REDIS_PORT)
        self.test_message_key = "chriskingtestkey"
        self.test_message_body = "Today is a great day for connectivity!"
        
    def test_connectivity(self):
        """
        Receiving a None value for a blank fetch, ensures that there is connectivity to the
        cluster. This is all that we need to do in order to validate the credentials worked.
        """
        try:
            self.assertIsNone(self.redis.get(None))  # getting None returns None or throws an exception
        except (redis.exceptions.ConnectionError, 
                redis.exceptions.BusyLoadingError):
            return False
        return True

    def test_send_a_message(self):
        """
        First we are going to declare a test value, then we will send it to the 
        Redis cluster. If the client does not throw an exception, the message was sent successfully.

        We will test for receiving in the next test.
        """
        
        self.assertTrue(self.redis.set(self.test_message_key, self.test_message_body))

    def test_receive_a_message(self):
        """
        This is going to retrieve the key after sending it.
        """
        self.redis.set(self.test_message_key, self.test_message_body)
        self.assertEquals(self.test_message_body, self.redis.get(self.test_message_key))


    def test_trigger_a_node_failure(self):
        """
        run() comes from Fabric, you can learn more here: http://www.fabfile.org/
        This library lets us execute remote shell commands. Firing off the reboot notice
        will trigger a failure in the cluster.

        We can then connect with a new redis client and validate the cluster is still behaving as expected.
        """
        # Rebooting is not treated nicely and throws an exception that you lost a connection
        try:
            with settings(host_string=SWARM_NODE_1, warn_only=True):
                run("reboot",shell=False)
        except Exception, e:
            pass
        self.redis2 = redis.Redis(host=SWARM_NODE_2, port=REDIS_PORT)
        self.redis2.set(self.test_message_key, self.test_message_body)
        self.assertEquals(self.test_message_body, self.redis2.get(self.test_message_key))
        self.redis2.delete(self.test_message_key)
        # Our bare metal instances have an off time of about 5 minutes so this test is going to sleep
        #for that long, please adjust accordingly.
        print "Sleeping for 5 minutes, this is to give the node a chance to come back."
        time.sleep(300)

    def test_usability_after_a_node_failure(self):
        """
        After a reboot, this test checks to see if messages can still be sent and 
        received. Proving that the Redis cluster is operational again.
        """
        self.redis.set(self.test_message_key, self.test_message_body)
        self.assertEquals(self.test_message_body, self.redis.get(self.test_message_key))

    def test_zkill_everything(self):
        """
        This test is going to reboot all 3 nodes for Redis, sleep then validate
        messages can be sent to them again.
        """
        try:
            with settings(host_string=SWARM_NODE_1, warn_only=True):
                run("reboot",shell=False)
        except Exception, e:
            pass
        try:
            with settings(host_string=SWARM_NODE_2, warn_only=True):
                run("reboot",shell=False)
        except Exception, e:
            pass
        try:
            with settings(host_string=SWARM_NODE_3, warn_only=True):
                run("reboot",shell=False)
        except Exception, e:
            pass
        print "Sleeping for 5 minutes to give the nodes a chance to come back."
        time.sleep(360)
        # Test Node 1
        self.redis = redis.Redis(host=SWARM_NODE_1, port=REDIS_PORT)
        self.redis.set(self.test_message_key, self.test_message_body)
        self.assertEquals(self.test_message_body, self.redis.get(self.test_message_key))
        # Test Node 2
        self.redis2 = redis.Redis(host=SWARM_NODE_2, port=REDIS_PORT)
        self.redis2.set(self.test_message_key, self.test_message_body)
        self.assertEquals(self.test_message_body, self.redis2.get(self.test_message_key))
        self.redis2.delete(self.test_message_key)
        # Test Node 3
        self.redis3 = redis.Redis(host=SWARM_NODE_3, port=REDIS_PORT)
        self.redis3.set(self.test_message_key, self.test_message_body)
        self.assertEquals(self.test_message_body, self.redis3.get(self.test_message_key))
        self.redis3.delete(self.test_message_key)
        
    def tearDown(self):
        """
        The items here ensure that Redis is in a good state after all of the testing
        has been completed.
        """
        self.redis.delete(self.test_message_key)

if __name__ == '__main__':
    unittest.main()

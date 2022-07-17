import asyncio
import pytest
import pytest_asyncio
import json
import sapling.utils.ptp as ptp
import binascii

@pytest_asyncio.fixture
def ptp_object(mocker):
    reader = mocker.MagicMock()
    writer = mocker.MagicMock()

    reader.configure_mock(
        **{
            "readline.return_value": "test",
        }
    )

    return ptp.AsyncPacketTransferProtocol(reader, writer)

class TestAsyncPacketTransferProtocol:
    
    def test_create_packet(self, ptp_object):
        test_string = "hello"
        test_packet = ptp_object._create_packet(test_string)
        reload = json.loads(test_packet.decode('ascii'))
        assert reload['d'] == test_string
        assert reload['c'] ==  binascii.crc32(test_string.encode('ascii'), 0)

    def test_crc32_packet(self, ptp_object):
        test_packet = {'d': "hello"}
        assert ptp_object.crc32_packet(test_packet) == binascii.crc32("hello".encode('ascii'), 0)

    @pytest_asyncio.fixture
    def create_test_packet(self, ptp_object):
        test_string = "hello"
        bin_packet = ptp_object._create_packet(test_string)
        future_packet = asyncio.Future()
        future_packet.set_result(bin_packet + b'\n')
        return future_packet, bin_packet, test_string

    @pytest.mark.asyncio
    async def test_receive_packet(self, ptp_object, create_test_packet):
        future_packet, bin_packet, test_string = create_test_packet
        
        ptp_object.reader.configure_mock(
            **{
                "readline.return_value": future_packet,
            }
        )
        received_packet = await ptp_object._receive_packet()
        # check if the packet is in the Queue
        assert await ptp_object.inbox.get() == test_string
        # also check it if was returned
        assert received_packet == test_string

    @pytest.mark.asyncio
    async def test_wait_for_ack(self, ptp_object, create_test_packet):
        future_packet, bin_packet, test_string = create_test_packet
        timeout = 0.00000001
        ptp_object.reader.configure_mock(
            **{
                "readline.return_value": future_packet,
            }
        )
        # success
        data = await ptp_object._wait_for_ack(timeout)

    @pytest.mark.asyncio
    async def test_send_packet(self, mocker, ptp_object, create_test_packet):
        future_packet, bin_packet, test_string = create_test_packet
        mocker.patch(ptp_object._wait_for_ack, )
        ptp_object._send_packet(test_string)
        assert ptp_object.writer.write.called_once_with(bin_packet)

    def test_send(self, ptp_object):
        pass

    def test_receive(self, ptp_object):
        pass
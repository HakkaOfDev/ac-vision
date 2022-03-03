import PageLayout from '@/components/page-layout';
import {
  Box,
  Button,
  Circle,
  Heading,
  HStack,
  Image,
  Table,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
  useToast,
  VStack,
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';

type DeviceProps = {
  model: string;
  onuId?: number;
  displayName: string;
  macAddress: string;
  ipAddress: string;
  uptime: string;
  inactiveTime: string;
  status: string;
  rxPower?: number;
  distance?: number;
  gponPort?: number;
  serialNumber?: string;
  temperature?: number;
  profile?: string;
};

const DeviceItem = ({
  model,
  onuId,
  displayName,
  macAddress,
  ipAddress,
  inactiveTime,
  uptime,
  status,
  rxPower,
  distance,
  gponPort,
  serialNumber,
  temperature,
  profile,
}: DeviceProps) => {
  const isActive = status === 'active';

  return (
    <Tr>
      <Td>
        <HStack spacing={3}>
          <Circle size='10px' bg={isActive ? 'green.300' : 'red.300'} />
          <Image src={`/assets/images/models/${model}.png`} h={16} />
        </HStack>
      </Td>
      <Td>
        <Text>{displayName}</Text>
      </Td>
      <Td>
        <Text>{macAddress}</Text>
      </Td>
      <Td>
        <Text>{ipAddress}</Text>
      </Td>
      <Td>{distance && <Text>{distance}m</Text>}</Td>
      <Td>
        {rxPower && (
          <Button
            variant='ghost'
            size='sm'
            colorScheme={
              rxPower < -25 ? 'red' : rxPower > -15 ? 'green' : 'yellow'
            }
          >
            {rxPower} dBm
          </Button>
        )}
      </Td>
      <Td>
        <Button
          variant='ghost'
          size='sm'
          colorScheme={isActive ? 'green' : 'red'}
        >
          {isActive ? uptime : inactiveTime}
        </Button>
      </Td>
      <Td>
        <Button
          variant='outline'
          rounded='full'
          size='sm'
          colorScheme={isActive ? 'green' : 'red'}
          disabled
        >
          {isActive ? 'Connected' : 'Disconnected'}
        </Button>
      </Td>
      <Td>{gponPort && <Text>{gponPort}</Text>}</Td>
      <Td>{serialNumber && <Text>{serialNumber}</Text>}</Td>
      <Td>{profile && <Text>{profile}</Text>}</Td>
      <Td>{temperature && <Text>{temperature}°</Text>}</Td>
    </Tr>
  );
};

const DevicesPage = () => {
  const [devices, setDevices] = useState<DeviceProps[]>([]);
  const toast = useToast();
  useEffect(() => {
    updateOnus(false);
  }, []);

  const updateOnus = async (userInteraction: boolean) => {
    const req = await fetch('http://ac-vision/api/v1.0/ressources/devices');
    if (req.status === 404) {
      toast({
        title: 'An error occured',
        description: 'The cache is not updating, please wait few seconds.',
        status: 'error',
        duration: 2000,
      });
    } else if (req.status === 200) {
      const devicesList: DeviceProps[] = await req.json();
      setDevices(devicesList);
      if (userInteraction) {
        toast({
          description: 'Devices were successfully updated.',
          duration: 1500,
          status: 'success',
        });
      }
    } else {
      toast({
        title: 'An error occured',
        description: 'Please contact an administrator.',
        status: 'error',
        duration: 2000,
      });
    }
  };

  return (
    <PageLayout title='Devices' description='Tables with devices'>
      <VStack spacing={4} w='100%' overflow='auto' py={4}>
        <Heading>Devices</Heading>
        <Box w='100%' overflowX='scroll'>
          <Table variant='simple' size='sm'>
            <Thead>
              <Tr>
                <Th>TYPE</Th>
                <Th>DISPLAY NAME</Th>
                <Th>MAC ADDRESS</Th>
                <Th>IP ADDRESS</Th>
                <Th>DISTANCE</Th>
                <Th w={24}>SIGNAL</Th>
                <Th w={24}>UPTIME</Th>
                <Th>STATUS</Th>
                <Th>GPON PORT</Th>
                <Th>SERIAL NUMBER</Th>
                <Th>PROFILE</Th>
                <Th>TEMPERATURE</Th>
              </Tr>
            </Thead>
            <Tbody>
              {devices.length !== 0 &&
                devices.map((device) => (
                  <DeviceItem key={device.displayName} {...device} />
                ))}
            </Tbody>
          </Table>
        </Box>
        <Button onClick={() => updateOnus(true)}>Update</Button>
      </VStack>
    </PageLayout>
  );
};

export default DevicesPage;

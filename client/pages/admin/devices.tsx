import PageLayout from '@/components/page-layout';
import {
  Button,
  HStack,
  Image,
  SkeletonCircle,
  Table,
  TableCaption,
  Tbody,
  Td,
  Text,
  Th,
  Thead,
  Tr,
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
        <HStack>
          <SkeletonCircle size='4' startColor={isActive ? 'green' : 'red'} />
          <Image src={`/assets/images/models/${model}.png`} h={12} />
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
          <Text
            color={rxPower < -25 ? 'red' : rxPower > -15 ? 'green' : 'yellow'}
          >
            {rxPower} dBm
          </Text>
        )}
      </Td>
      <Td>
        <Text color={isActive ? 'green' : 'red'}>
          {isActive ? uptime : inactiveTime}
        </Text>
      </Td>
      <Td>
        <Button
          variant='outline'
          rounded='full'
          colorScheme={isActive ? 'green' : 'red'}
          disabled
        >
          {isActive ? 'Connected' : 'Disconnected'}
        </Button>
      </Td>
      <Td>{gponPort && <Text>{gponPort}</Text>}</Td>
      <Td>{serialNumber && <Text>{serialNumber}</Text>}</Td>
      <Td>{temperature && <Text>{temperature}°</Text>}</Td>
      <Td>{profile && <Text>{profile}</Text>}</Td>
    </Tr>
  );
};

const DevicesPage = () => {
  const [devices, setDevices] = useState<DeviceProps[]>([]);

  useEffect(() => {
    updateOnus();
  }, []);

  const updateOnus = async () => {
    const req = await fetch('http://ac-vision/api/v1.0/ressources/devices');
    const devicesList: DeviceProps[] = await req.json();
    console.log(devicesList);
    setDevices(devicesList);
  };

  return (
    <PageLayout title='Devices' description='Tables with devices'>
      <VStack spacing={4} w='100%' overflowX='scroll'>
        <Table size='sm'>
          <TableCaption>Dasan Devices</TableCaption>
          <Thead>
            <Tr>
              <Th>TYPE</Th>
              <Th>NAME</Th>
              <Th>MAC ADDRESS</Th>
              <Th>IP ADDRESS</Th>
              <Th>DISTANCE</Th>
              <Th>SIGNAL</Th>
              <Th>UPTIME</Th>
              <Th>STATUS</Th>
              <Th>GPON PORT</Th>
              <Th>SERIAL NUMBER</Th>
              <Th>TEMPERATURE</Th>
              <Th>PROFILE</Th>
            </Tr>
          </Thead>
          <Tbody>
            {devices.length !== 0 &&
              devices.map((device) => (
                <DeviceItem key={device.displayName} {...device} />
              ))}
          </Tbody>
        </Table>
        <Button onClick={updateOnus}>Update</Button>
      </VStack>
    </PageLayout>
  );
};

export default DevicesPage;
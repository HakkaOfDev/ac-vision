import { Onu } from '@/types/Onu';
import {
  HStack,
  Image,
  Popover,
  PopoverArrow,
  PopoverBody,
  PopoverCloseButton,
  PopoverContent,
  PopoverHeader,
  PopoverTrigger,
  Text,
  useBreakpointValue,
  useColorModeValue,
  VStack,
} from '@chakra-ui/react';

const PopItem = ({ label, value }) => {
  return (
    <HStack>
      <Text fontSize='lg' color={useColorModeValue('gray.900', 'white')}>
        {label}:{' '}
        <Text as='span' color='acvision'>
          {value}
        </Text>
      </Text>
    </HStack>
  );
};

const OnuItem = ({
  id,
  onuId,
  displayName,
  model,
  serialNumber,
  gponPort,
  macAddress,
  ipAddress,
  uptime,
  status,
  rxPower,
  profile,
  distance,
}: Onu) => {
  const isMobile = useBreakpointValue({ base: true, lg: false });

  return (
    <Popover trigger={isMobile ? 'click' : 'hover'} gutter={16}>
      <PopoverTrigger>
        <VStack>
          <Image
            src={`/assets/images/models/${model}.png`}
            alt={`Thumbail of ${id} devices`}
            h={50}
            w={50}
          />
          <Text>{displayName === '' ? serialNumber : displayName}</Text>
          <Text fontSize='lg'>{onuId}</Text>
        </VStack>
      </PopoverTrigger>
      <PopoverContent>
        <PopoverArrow />
        <PopoverCloseButton />
        <PopoverHeader>
          <Text fontSize='xl' color={useColorModeValue('brand.500', 'white')}>
            Details
          </Text>
        </PopoverHeader>
        <PopoverBody>
          <VStack justify='start'>
            <PopItem
              label='Name'
              value={displayName === '' ? serialNumber : displayName}
            />
            <PopItem label='Gpon Port' value={gponPort} />
            <PopItem label='Profile' value={profile} />
            <PopItem label='Ip Address' value={ipAddress} />
            <PopItem label='Mac Address' value={macAddress} />
            <PopItem label='Status' value={status} />
            <PopItem label='Signal' value={`${rxPower} dBm`} />
            <PopItem label='Distance' value={`${distance}m`} />
            <PopItem label='Uptime' value={uptime} />
          </VStack>
        </PopoverBody>
      </PopoverContent>
    </Popover>
  );
};

export default OnuItem;

import { Olt } from '@/types/Olt';
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

const OltItem = ({
  id,
  displayName,
  model,
  macAddress,
  ipAddress,
  uptime,
  status,
  temperature,
}: Olt) => {
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
          <Text>{displayName}</Text>
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
            <PopItem label='Name' value={displayName} />
            <PopItem label='Ip Address' value={ipAddress} />
            <PopItem label='Mac Address' value={macAddress} />
            <PopItem label='Temperature' value={`${temperature}°`} />
            <PopItem label='Status' value={status} />
            <PopItem label='Uptime' value={uptime} />
          </VStack>
        </PopoverBody>
      </PopoverContent>
    </Popover>
  );
};

export default OltItem;

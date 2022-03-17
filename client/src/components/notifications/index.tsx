import { Notification } from '@/types/Notifications';
import { Heading, HStack, StackProps, Text, VStack } from '@chakra-ui/react';
import { useEffect, useState } from 'react';

const NotificationCard = ({
  onuid,
  gponPort,
  status,
  reason,
  date,
}: Notification) => {
  const isRed = status === 'DEACTIVATION';

  return (
    <VStack
      spacing={1}
      padding={1}
      bgColor={isRed ? 'red.400' : 'green.400'}
      borderColor={isRed ? 'red.600' : 'green.600'}
      borderWidth={1}
      borderStart='solid'
      w='100%'
    >
      <Heading>
        [{status}] ONU {onuid} on gponPort {gponPort}
      </Heading>
      <HStack spacing={2}>
        <Text>
          <strong>Date: </strong>
          {date}
        </Text>
        {reason && (
          <Text>
            <strong>Date: </strong>
            {reason}
          </Text>
        )}
      </HStack>
    </VStack>
  );
};

const Notifications = ({...stackProps}: StackProps) => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  useEffect(() => {
    async function getNotifications() {
      const req = await fetch(
        'http://ac-vision/api/v1.0/ressources/notification'
      );
      const notifs: Notification[] = await req.json();
      setNotifications(notifs);
    }
    getNotifications();
  }, []);

  return (
    <VStack {...stackProps}>
      {notifications.map((notification) => (
        <NotificationCard {...notification} />
      ))}
    </VStack>
  );
};

export default Notifications;

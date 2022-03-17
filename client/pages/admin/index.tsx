import Notifications from '@/components/notifications';
import PageLayout from '@/components/page-layout';
import { Activity } from '@/types/Activity';
import { Heading, Stack, VStack } from '@chakra-ui/react';
import { ArcElement, Chart as ChartJS, Legend, Tooltip } from 'chart.js';
import { useEffect, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';

ChartJS.register(ArcElement, Tooltip, Legend);

const DashboardPage = () => {
  const [onusActivity, setOnusActivity] = useState<Activity>({
    active: 0,
    inactive: 0,
    total: 0,
  });

  useEffect(() => {
    async function getActivity() {
      const req = await fetch(
        'http://ac-vision/api/v1.0/ressources/dasan/onuactivity'
      );
      const activity: Activity = await req.json();
      setOnusActivity(activity);
    }
    getActivity();
  }, []);

  const data = {
    labels: ['active', 'inactive', 'total'],
    datasets: [
      {
        data: [onusActivity.active, onusActivity.inactive, onusActivity.total],
        backgroundColor: [
          'rgba(255, 99, 132, 0.2)',
          'rgba(54, 162, 235, 0.2)',
          'rgba(255, 206, 86, 0.2)',
        ],
        borderColor: [
          'rgba(255, 99, 132, 1)',
          'rgba(54, 162, 235, 1)',
          'rgba(255, 206, 86, 1)',
        ],
        borderWidth: 1,
      },
    ],
  };

  return (
    <PageLayout title='Dashboard' description='See your stats.'>
      <VStack spacing={2} justify='center'>
        <Heading>Dashboard</Heading>
        <Stack direction={{ base: 'column', lg: 'row' }} spacing={4}>
          <VStack w={{ base: '100%', lg: '50%' }} spacing={4}>
            <Heading>ONU's Activity</Heading>
            <Doughnut data={data} />
          </VStack>
          <VStack w={{ base: '100%', lg: '50%' }} spacing={4}>
            <Heading>Notifications</Heading>
            <Notifications spacing={1} overflowY='scroll' h='75vh' />
          </VStack>
        </Stack>
      </VStack>
    </PageLayout>
  );
};

export default DashboardPage;

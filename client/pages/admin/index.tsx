import Notifications from '@/components/notifications';
import PageLayout from '@/components/page-layout';
import { Activity } from '@/types/Activity';
import { Heading, Stack, VStack } from '@chakra-ui/react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
);

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
    labels: ['ACTIVES', 'INACTIVES', 'TOTAL'],
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

  const options = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top' as const,
      },
    },
  };

  return (
    <PageLayout title='Dashboard' description='See your stats.'>
      <VStack spacing={2} justify='center' w='100%'>
        <Heading>Dashboard</Heading>
        <Stack direction={{ base: 'column', lg: 'row' }} spacing={4} w='100%'>
          <VStack
            w={{ base: '100%', lg: '50%' }}
            spacing={4}
            justify='center'
            align='center'
          >
            <Heading fontSize='lg' w='100%' textAlign='center'>
              ONU's Activity
            </Heading>
            <Bar options={options} data={data} />
          </VStack>
          <VStack
            w={{ base: '100%', lg: '50%' }}
            spacing={4}
            justify='center'
            align='center'
          >
            <Heading fontSize='lg' w='100%' textAlign='center'>
              Notifications
            </Heading>
            <Notifications spacing={1} overflowY='scroll' h='70vh' />
          </VStack>
        </Stack>
      </VStack>
    </PageLayout>
  );
};

export default DashboardPage;

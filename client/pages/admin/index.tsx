import PageLayout from '@/components/page-layout';
import { Heading, VStack } from '@chakra-ui/react';

const DashboardPage = () => {
  return (
    <PageLayout title='Dashboard' description='See your stats.'>
      <VStack spacing={2} justify='center'>
        <Heading>Dashboard</Heading>
      </VStack>
    </PageLayout>
  );
};

export default DashboardPage;

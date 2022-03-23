import ExternalLink from '@/components/external-link';
import InlineLink from '@/components/inline-link';
import PageLayout from '@/components/page-layout';
import { Code, Heading, Text, VStack } from '@chakra-ui/react';

const DocumentationPage = () => {
  return (
    <PageLayout title='Settings' description='Manage your app.'>
      <VStack spacing={3} justify='start' w='100%'>
        <Heading>Documentation</Heading>
        <Heading fontSize='lg'>Installation</Heading>
        <Text>
          You can find a complete guide about the installation on the{' '}
          <ExternalLink href='https://github.com/HakkaOfDev/AC-Vision'>
            GitHub repository
          </ExternalLink>
          .
        </Text>
        <Heading fontSize='lg'>Workflow</Heading>
        <Text>
          The workflow have controls, zoom, a locker to lock the position of
          items and a resizer to fit the view. Go on{' '}
          <InlineLink href='/admin/workflow'>Map Page</InlineLink> and try by
          yourself.
        </Text>
        <Heading fontSize='lg'>Settings</Heading>
        <Text>
          Two seetings are presents on the application. The first is{' '}
          <Code>OLT IP</Code>, it permit to change the OLT IP in case the IP
          will be changed. To change it, go on{' '}
          <InlineLink href='/admin/settings'>Settings Page</InlineLink>, enter
          the new IP on the input and press on the button right on it.<br></br>
          The second is the <Code>ONU's displayName</Code>, same as first,
          select your ONU from his ID, insert his new displayName and press the
          button.
        </Text>
        <Heading fontSize='lg'>Theming</Heading>
        <Text>You can change your theme by clicking on the lune or sun icon on the top navbar.</Text>
      </VStack>
    </PageLayout>
  );
};

export default DocumentationPage;

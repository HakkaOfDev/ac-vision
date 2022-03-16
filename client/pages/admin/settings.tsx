import PageLayout from '@/components/page-layout';
import { Onu } from '@/types/Onu';
import {
  Button,
  Heading,
  HStack,
  Input,
  Select,
  Text,
  useToast,
  VStack,
} from '@chakra-ui/react';
import { FaAngleDoubleRight } from '@react-icons/all-files/fa/FaAngleDoubleRight';
import { useEffect, useState } from 'react';

type SettingIp = {
  id: number;
  value: string;
  name: string;
};

const SettingsPage = () => {
  const [newOltIp, setNewOltIp] = useState<string>('');
  const [onuId, setOnuId] = useState<string>('1');
  const [onuIDsList, setOnuIDsList] = useState<number[]>([]);
  const [newOnuDisplayName, setNewOnuDisplayName] = useState<string>('default');
  const toast = useToast();

  const getOltIp = async () => {
    const req = await fetch(
      'http://ac-vision/api/v1.0/ressources/dasan/setting/ip/'
    );
    const settingIp: SettingIp = await req.json();
    return settingIp.value;
  };

  const changeOltIp = async () => {
    const data = new FormData();
    data.append('name', 'ip_olt');
    data.append('value', newOltIp);

    const req = await fetch(
      'http://ac-vision/api/v1.0/ressources/dasan/setting/',
      { method: 'POST', body: data }
    );
    if (req.status == 200) {
      toast({
        title: `OLT IP was changed to ${newOltIp}`,
        status: 'success',
        duration: 2000,
      });
    } else {
      toast({
        title: 'An error occured.',
        description: 'Please contact an administrator.',
        status: 'error',
        duration: 2000,
      });
    }
  };

  const changeOnuDisplayName = async () => {
    const data = new FormData();
    data.append('onuid', onuId);
    data.append('description', newOnuDisplayName);

    const req = await fetch(
      'http://ac-vision/api/v1.0/ressources/dasan/desconu/',
      { method: 'POST', body: data }
    );
    if (req.status == 200) {
      toast({
        title: `Display name for onu ${onuId} was changed to : ${newOnuDisplayName}`,
        status: 'success',
        duration: 2000,
      });
    } else {
      toast({
        title: 'An error occured.',
        description: 'Please contact an administrator.',
        status: 'error',
        duration: 2000,
      });
    }
  };

  useEffect(() => {
    async function setOnuIdsListFromAPI() {
      const req = await fetch(
        'http://ac-vision/api/v1.0/ressources/dasan/onus'
      );
      const onusList: Onu[] = await req.json();
      setOnuIDsList(onusList.map(({ onuId }) => onuId));
    }
    setOnuIdsListFromAPI()
  }, []);

  return (
    <PageLayout title='Settings' description='Manage your app.'>
      <VStack spacing={4} justify='center'>
        <Heading>Settings</Heading>
        <HStack boxShadow='lg' spacing={2}>
          <Text>OLT IP</Text>
          <Input
            variant='outline'
            placeholder={`${getOltIp}`}
            onChange={(e) => setNewOltIp(e.target.value)}
          />
          <Button
            rightIcon={<FaAngleDoubleRight />}
            colorScheme='brand'
            variant='solid'
            onClick={changeOltIp}
          ></Button>
        </HStack>
        <HStack boxShadow='lg' spacing={2}>
          <Text>ONU's NAME</Text>
          <Select
            variant='outline'
            placeholder='Select an ONU id'
            onChange={(e) => setOnuId(e.currentTarget.value)}
          >
            {onuIDsList.map((id) => (
              <option key={id} value={id}>
                {id}
              </option>
            ))}
          </Select>
          <Input
            variant='outline'
            placeholder='New onu display name'
            onChange={(e) => setNewOnuDisplayName(e.target.value)}
          />
          <Button
            rightIcon={<FaAngleDoubleRight />}
            colorScheme='brand'
            variant='solid'
            onClick={changeOnuDisplayName}
          ></Button>
        </HStack>
      </VStack>
    </PageLayout>
  );
};

export default SettingsPage;

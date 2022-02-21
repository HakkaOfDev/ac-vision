import {
  Button,
  Image,
  Input,
  InputGroup,
  InputLeftElement,
  Stack,
  useToast,
  VStack,
} from '@chakra-ui/react';
import { BiKey } from '@react-icons/all-files/bi/BiKey';
import { BiUserCircle } from '@react-icons/all-files/bi/BiUserCircle';
import { FaAngleDoubleRight } from '@react-icons/all-files/fa/FaAngleDoubleRight';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';

const IndexPage = () => {
  const toast = useToast();
  const router = useRouter();
  const [login, setLogin] = useState<string>();
  const [password, setPassword] = useState<string>();

  useEffect(() => {
    const user = localStorage.getItem('user');
    if (user) {
      router.push('/admin');
    }
  }, []);

  const auth = async () => {
    const data = new FormData();
    data.append('username', login);
    data.append('password', password);

    await fetch('http://ac-vision/api/v1.0/ressources/login/token', {
      method: 'POST',
      body: data,
    }).then((res) => {
      if (res.status === 200) {
        res.json().then(({ access_token, message }) => {
          toast({
            description: message,
            status: 'success',
            duration: 1000,
            onCloseComplete: () => {
              fetch('http://ac-vision/api/v1.0/ressources/users/me', {
                headers: {
                  Accept: 'application/json',
                  Authorization: 'Bearer ' + access_token,
                },
              }).then((res) => {
                res
                  .json()
                  .then(({ first_name, last_name, email, role, login }) => {
                    localStorage.setItem(
                      'user',
                      JSON.stringify({
                        firstName: first_name,
                        lastName: last_name,
                        email: email,
                        role: role,
                        login: login,
                        token: access_token,
                      })
                    );
                    router.push('/admin');
                  });
              });
            },
          });
        });
      } else {
        toast({
          description: 'Invalid credentials. Please try again...',
          status: 'error',
          duration: 1500,
        });
      }
    });
  };

  return (
    <Stack
      spacing={4}
      py={12}
      align='center'
      w='100%'
      h='100vh'
      direction={{ base: 'column', md: 'row' }}
    >
      <VStack
        w={{ base: '100%', md: '25%' }}
        px={4}
        justify='center'
        align='center'
        spacing={3}
      >
        <Image src='/assets/images/logo_blanc.png' alt='Logo' />
        <InputGroup>
          <InputLeftElement pointerEvents='none' children={<BiUserCircle />} />
          <Input
            variant='outline'
            placeholder='Login'
            onChange={(e) => setLogin(e.target.value)}
          />
        </InputGroup>
        <InputGroup>
          <InputLeftElement pointerEvents='none' children={<BiKey />} />
          <Input
            variant='outline'
            type='password'
            placeholder='Password'
            onChange={(e) => setPassword(e.target.value)}
          />
        </InputGroup>
        <Button
          rightIcon={<FaAngleDoubleRight />}
          colorScheme='brand'
          variant='solid'
          onClick={() => auth()}
        >
          Login
        </Button>
      </VStack>
      <Image
        h='100vh'
        fit='cover'
        w={{ base: '100%', md: '75%' }}
        src='/assets/images/background.jpg'
        alt='Background'
      />
    </Stack>
  );
};

export default IndexPage;

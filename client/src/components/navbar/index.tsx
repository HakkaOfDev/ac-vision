import { User } from '@/types/User';
import {
  Avatar,
  Box,
  BoxProps,
  Button,
  CloseButton,
  Drawer,
  DrawerContent,
  Flex,
  FlexProps,
  HStack,
  Icon,
  IconButton,
  Image,
  Link,
  Popover,
  PopoverArrow,
  PopoverBody,
  PopoverCloseButton,
  PopoverContent,
  PopoverHeader,
  PopoverTrigger,
  Text,
  useColorModeValue,
  useDisclosure,
  useToast,
  VStack,
} from '@chakra-ui/react';
import { BiNetworkChart } from '@react-icons/all-files/bi/BiNetworkChart';
import { CgViewComfortable } from '@react-icons/all-files/cg/CgViewComfortable';
import { FiBell } from '@react-icons/all-files/fi/FiBell';
import { FiMenu } from '@react-icons/all-files/fi/FiMenu';
import { FiSettings } from '@react-icons/all-files/fi/FiSettings';
import { GoSignOut } from '@react-icons/all-files/go/GoSignOut';
import { IconType } from '@react-icons/all-files/lib';
import { MdDashboard } from '@react-icons/all-files/md/MdDashboard';
import NextLink from 'next/link';
import { useRouter } from 'next/router';
import React, { ReactText, useEffect, useState } from 'react';
import Notifications from '../notifications';
import ThemeButton from '../theme-button';

type LinkItem = {
  name: string;
  icon: IconType;
  href: string;
};

const linkItems: LinkItem[] = [
  { name: 'Dashboard', icon: MdDashboard, href: '/admin' },
  { name: 'Workflow', icon: BiNetworkChart, href: '/admin/workflow' },
  { name: 'Devices', icon: CgViewComfortable, href: '/admin/devices' },
  { name: 'Settings', icon: FiSettings, href: '/admin/settings' },
];

const SidebarWithHeader = ({ children }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [user, setUser] = useState<User>();
  const router = useRouter();

  useEffect(() => {
    const session: string = localStorage.getItem('user');
    if (!session) {
      router.push('/');
    } else {
      const userItem: User = JSON.parse(session);
      setUser(userItem);
    }
  }, []);

  return (
    <Box minH='100vh' bg={useColorModeValue('gray.100', 'gray.900')}>
      <SidebarContent
        onClose={() => onClose}
        display={{ base: 'none', md: 'block' }}
      />
      <Drawer
        autoFocus={false}
        isOpen={isOpen}
        placement='left'
        onClose={onClose}
        returnFocusOnClose={false}
        onOverlayClick={onClose}
        size='full'
      >
        <DrawerContent>
          <SidebarContent onClose={onClose} />
        </DrawerContent>
      </Drawer>
      <MobileNav user={user} onOpen={onOpen} />
      <Box ml={{ base: 0, md: 60 }} p='4' as='main'>
        {children}
      </Box>
    </Box>
  );
};

interface SidebarProps extends BoxProps {
  onClose: () => void;
}

const SidebarContent = ({ onClose, ...rest }: SidebarProps) => {
  const router = useRouter();
  const toast = useToast();

  const logout = () => {
    toast({
      description: "You're now logout, waiting redirection...",
      status: 'success',
      duration: 1000,
      onCloseComplete: () => {
        localStorage.removeItem('user');
        router.push('/');
      },
    });
  };

  return (
    <Flex
      transition='1s ease'
      bg={useColorModeValue('white', 'gray.900')}
      borderRight='1px'
      borderRightColor={useColorModeValue('gray.200', 'gray.700')}
      direction='column'
      w={{ base: 'full', md: 60 }}
      pos='fixed'
      h='full'
      {...rest}
    >
      <Flex
        h='20'
        alignItems='center'
        mx={8}
        my={4}
        justifyContent='space-between'
      >
        <Image
          src={`/assets/images/logo_${useColorModeValue('bleu', 'blanc')}.png`}
          alt='Logo'
        />
        <CloseButton display={{ base: 'flex', md: 'none' }} onClick={onClose} />
      </Flex>
      {linkItems.map(({ name, icon, href }) => (
        <NavItem key={name} icon={icon} href={href}>
          {name}
        </NavItem>
      ))}
      <Button
        leftIcon={<GoSignOut />}
        onClick={() => logout()}
        colorScheme='red'
        variant='ghost'
        size='md'
        w='100%'
      >
        Sign out
      </Button>
    </Flex>
  );
};

interface NavItemProps extends FlexProps {
  icon: IconType;
  href: string;
  children: ReactText;
}
const NavItem = ({ icon, href, children, ...rest }: NavItemProps) => {
  return (
    <NextLink href={href} passHref>
      <Link style={{ textDecoration: 'none' }} _focus={{ boxShadow: 'none' }}>
        <Flex
          align='center'
          p='4'
          mx='4'
          borderRadius='lg'
          role='group'
          cursor='pointer'
          _hover={{
            bg: 'acvision',
            color: 'white',
          }}
          {...rest}
        >
          {icon && (
            <Icon
              mr='4'
              fontSize='16'
              _groupHover={{
                color: 'white',
              }}
              as={icon}
            />
          )}
          {children}
        </Flex>
      </Link>
    </NextLink>
  );
};

interface MobileProps extends FlexProps {
  user: User;
  onOpen: () => void;
}
const MobileNav = ({ user, onOpen, ...rest }: MobileProps) => {
  return (
    <Flex
      ml={{ base: 0, md: 60 }}
      px={{ base: 4, md: 4 }}
      height='20'
      alignItems='center'
      bg={useColorModeValue('white', 'gray.900')}
      borderBottomWidth='1px'
      borderBottomColor={useColorModeValue('gray.200', 'gray.700')}
      justifyContent={{ base: 'space-between', md: 'flex-end' }}
      {...rest}
    >
      <IconButton
        display={{ base: 'flex', md: 'none' }}
        onClick={onOpen}
        variant='outline'
        aria-label='open menu'
        icon={<FiMenu />}
      />

      <Image
        src={`/assets/images/logo_${useColorModeValue('bleu', 'blanc')}.png`}
        alt='Logo'
        h={14}
        display={{ base: 'flex', md: 'none' }}
      />

      <HStack spacing={{ base: '0', md: '3' }}>
        <Popover>
          <PopoverTrigger>
            <IconButton
              size='lg'
              variant='ghost'
              aria-label='Open menu'
              icon={<FiBell />}
            />
          </PopoverTrigger>
          <PopoverContent>
            <PopoverArrow />
            <PopoverCloseButton />
            <PopoverHeader>Notifications</PopoverHeader>
            <PopoverBody>
              <Notifications />
            </PopoverBody>
          </PopoverContent>
        </Popover>
        <ThemeButton />
        <Flex alignItems={'center'}>
          <HStack>
            <Avatar
              size={'sm'}
              src={`https://eu.ui-avatars.com/api/?name=${
                user?.firstName + '+' + user?.lastName
              }`}
            />
            <VStack
              display={{ base: 'none', md: 'flex' }}
              alignItems='flex-start'
              spacing='1px'
              ml='2'
            >
              <Text fontSize='sm'>
                {user?.firstName + ' ' + user?.lastName}
              </Text>
              <Text fontSize='xs' color='gray.600'>
                {user?.role}
              </Text>
            </VStack>
          </HStack>
        </Flex>
      </HStack>
    </Flex>
  );
};

export default SidebarWithHeader;

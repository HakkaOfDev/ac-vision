import {
  IconButton,
  useColorMode,
  useColorModeValue as mode,
} from '@chakra-ui/react';
import { BsMoon } from '@react-icons/all-files/bs/BsMoon';
import { WiDaySunny } from '@react-icons/all-files/wi/WiDaySunny';

const ThemeButton = () => {
  const { toggleColorMode } = useColorMode();

  return (
    <IconButton
      aria-label='Toggle color mode'
      key={mode('light', 'dark')}
      variant='ghost'
      size='lg'
      icon={mode(<BsMoon />, <WiDaySunny />)}
      onClick={toggleColorMode}
    />
  );
};

export default ThemeButton;

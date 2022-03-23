import { Link, LinkProps, useColorModeValue as mode } from '@chakra-ui/react';

const InlineLink = ({ children, ...linkProps }: LinkProps) => {
  return (
    <span>
      <Link
        {...linkProps}
        color={mode('brand.500', 'brand.300')}
        display='inline-flex'
      >
        {children}
      </Link>
    </span>
  );
};

export default InlineLink;

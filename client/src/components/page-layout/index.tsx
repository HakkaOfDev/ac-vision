import { Container, ContainerProps } from '@chakra-ui/react';
import { motion, Variants } from 'framer-motion';
import { NextSeo } from 'next-seo';
import { ReactNode } from 'react';
import SidebarWithHeader from '../navbar';

const variants: Variants = {
  hidden: {
    opacity: 0,
    x: 0,
    y: -40,
    transition: { duration: 0.4, type: 'easeOut' },
  },
  enter: {
    opacity: 1,
    x: 0,
    y: 0,
    transition: { duration: 0.4, type: 'easeOut' },
  },
  exit: {
    opacity: 0,
    x: -0,
    y: 40,
    transition: { duration: 0.4, type: 'easeOut' },
  },
};

type PageProps = {
  title: string;
  description?: string;
  children: ReactNode;
};

const MotionContainer = motion<ContainerProps>(Container);

const PageLayout = ({ title, description, children }: PageProps) => {
  return (
    <>
      <NextSeo
        title={title + ' | AC-Vision'}
        description={description}
        additionalLinkTags={[
          {
            rel: 'icon',
            href: '/favicon.ico',
          },
        ]}
      />
      <SidebarWithHeader>
        <MotionContainer
          display='flex'
          maxW='container.xl'
          px={{ base: 4 }}
          initial='hidden'
          animate='enter'
          exit='exit'
          variants={variants}
          centerContent
        >
          {children}
        </MotionContainer>
      </SidebarWithHeader>
    </>
  );
};

export default PageLayout;

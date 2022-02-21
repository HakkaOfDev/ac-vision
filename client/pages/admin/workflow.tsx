import OltItem from '@/components/devices/olt';
import OnuItem from '@/components/devices/onu';
import PageLayout from '@/components/page-layout';
import { Map } from '@/types/Map';
import { User } from '@/types/User';
import { Button, Heading, VStack } from '@chakra-ui/react';
import dagre from 'dagre';
import { useEffect, useState } from 'react';
import ReactFlow, {
  Background,
  ConnectionLineType,
  Controls,
  Edge,
  Elements,
  isNode,
  Node,
  Position,
} from 'react-flow-renderer';

const WorkflowPage = () => {
  const [user, setUser] = useState<User>();
  const [elements, setElements] = useState<Elements>([]);

  const getLayoutedElements = (elem: Elements) => {
    const dagreGraph = new dagre.graphlib.Graph();
    dagreGraph.setDefaultEdgeLabel(() => ({}));
    dagreGraph.setGraph({ rankdir: 'TB' });
    const width = 150;
    const height = 100;

    elem.forEach((el) => {
      if (isNode(el)) {
        dagreGraph.setNode(el.id, {
          width,
          height,
        });
      } else {
        dagreGraph.setEdge(el.source, el.target);
      }
    });

    dagre.layout(dagreGraph);

    return elem.map((el) => {
      if (isNode(el)) {
        const nodeWithPosition = dagreGraph.node(el.id);
        el.targetPosition = Position.Top;
        el.sourcePosition = Position.Bottom;
        el.position = {
          x: nodeWithPosition.x - width / 2 + Math.random() / 1000,
          y: nodeWithPosition.y - height / 2,
        };
      }
      return el;
    });
  };

  const updateNetwork = async () => {
    const req = await fetch('http://ac-vision/api/v1.0/ressources/map', {
      headers: {
        Authorization: 'Bearer ' + user?.token,
      },
    });
    const map: Map = await req.json();
    const elementsArray: Elements = [];

    map.onus.forEach((onu) => {
      elementsArray.push({
        id: `${onu.id}`,
        type: 'output',
        connectable: false,
        data: {
          label: (
            <>
              <OnuItem {...onu} />
            </>
          ),
        },
        style: {
          border: onu.status === 'active' ? '1px solid green' : '1px solid red',
        },
        position: { x: 0, y: 0 },
      } as Node);
    });

    map.olts.forEach((olt) => {
      elementsArray.push({
        id: `${olt.id}`,
        type: 'input',
        connectable: false,
        data: {
          label: (
            <>
              <OltItem {...olt} />
            </>
          ),
        },
        position: { x: 200, y: 0 },
      } as Node);
    });

    map.edges.forEach((edge) => {
      elementsArray.push({
        id: `e${edge.from}-${edge.to}`,
        source: `${edge.from}`,
        target: `${edge.to}`,
        animated: true,
        style: {
          stroke: edge.status === 'active' ? 'green' : 'red',
        },
      } as Edge);
    });

    setElements(getLayoutedElements(elementsArray));
    console.log('Elements updated');
    console.log(elements);
  };

  useEffect(() => {
    const userItem: User = JSON.parse(localStorage.getItem('user'));
    setUser(userItem);
  }, []);

  return (
    <PageLayout title='Workflow' description='See the map.'>
      <VStack w='100%' h='80vh' spacing={4} justify='center' p={4}>
        <Heading>Workflow</Heading>
        <ReactFlow
          elements={elements}
          onLoad={updateNetwork}
          snapToGrid={true}
          snapGrid={[20, 20]}
          defaultZoom={0.7}
          minZoom={0.1}
          maxZoom={3}
          connectionLineType={ConnectionLineType.SmoothStep}
        >
          <Controls />
          <Background color='#aaa' gap={16} />
        </ReactFlow>
        <Button onClick={updateNetwork}>Update</Button>
      </VStack>
    </PageLayout>
  );
};

export default WorkflowPage;

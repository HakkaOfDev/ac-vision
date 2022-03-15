import OltItem from '@/components/devices/olt';
import OnuItem from '@/components/devices/onu';
import PageLayout from '@/components/page-layout';
import { Map } from '@/types/Map';
import { Button, Heading, useToast, VStack } from '@chakra-ui/react';
import dagre from 'dagre';
import { useEffect, useState } from 'react';
import ReactFlow, {
  Background,
  ConnectionLineType,
  Controls,
  Edge,
  Elements,
  isNode,
  MiniMap,
  Node,
  Position,
} from 'react-flow-renderer';
import socketIOClient from 'socket.io-client';

const WorkflowPage = () => {
  const [elements, setElements] = useState<Elements>([]);
  const ENDPOINT = 'http://ac-vision:6969';
  const toast = useToast();

  useEffect(() => {
    const socket = socketIOClient(ENDPOINT, {
      transports: ['websocket', 'polling', 'flashsocket'],
    });
    socket.on('connection', (socket) => {
      console.log('connected to the server');
    });
    socket.on('ONU', (data) => {
      console.log(data);
      fetch('http://ac-vision/api/v1.0/ressources/map/update');
      updateNetwork();
    });
  }, []);

  const getLayoutedElements = (elem: Elements) => {
    const dagreGraph = new dagre.graphlib.Graph();
    dagreGraph.setDefaultEdgeLabel(() => ({}));
    dagreGraph.setGraph({ rankdir: 'TB' });
    const width = 200;
    const height = 150;

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
          x: nodeWithPosition.x - width / 2,
          y: nodeWithPosition.y - height / 2,
        };
      }
      return el;
    });
  };

  const updateNetwork = async () => {
    const req = await fetch('http://ac-vision/api/v1.0/ressources/map');
    if (req.status === 404) {
      toast({
        title: 'An error occured',
        description: 'The cache is not updating, please wait few seconds.',
        status: 'error',
        duration: 2000,
      });
    } else if (req.status === 200) {
      const map: Map = await req.json();
      const elementsArray: Elements = [];

      map.onus.forEach((onu) => {
        elementsArray.push({
          id: `${onu.id}`,
          type: 'output',
          connectable: false,
          className: onu.status,
          data: {
            label: (
              <>
                <OnuItem {...onu} />
              </>
            ),
          },
          style: {
            border:
              onu.status === 'active' ? '2px solid green' : '2px solid red',
          },
          position: { x: 0, y: 0 },
        } as Node);
      });

      map.olts.forEach((olt) => {
        elementsArray.push({
          id: `${olt.id}`,
          type: 'input',
          connectable: false,
          className: olt.status,
          data: {
            label: (
              <>
                <OltItem {...olt} />
              </>
            ),
          },
          style: {
            border:
              olt.status === 'active' ? '2px solid green' : '2px solid red',
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
      toast({
        description: 'Map updated with success !',
        status: 'success',
        duration: 1500,
      });
    } else {
      toast({
        title: 'An error occured',
        description: 'Please contact an administrator.',
        status: 'error',
        duration: 2000,
      });
    }
  };

  const onLoad = (reactFlowInstance) => {
    updateNetwork();
    reactFlowInstance.fitView({ padding: 0.2, includeHiddenNodes: true });
  };

  return (
    <PageLayout title='Workflow' description='See the map.'>
      <VStack w='100%' h='80vh' spacing={4} justify='center' p={4}>
        <Heading>Workflow</Heading>
        <ReactFlow
          style={{ width: '100%' }}
          elements={elements}
          onLoad={onLoad}
          snapToGrid={true}
          snapGrid={[20, 20]}
          defaultZoom={0.9}
          minZoom={0.1}
          maxZoom={3}
          connectionLineType={ConnectionLineType.SmoothStep}
        >
          <MiniMap
            nodeStrokeColor={(n: Node) => {
              if (n.className === 'active') {
                return 'darkgreen';
              } else {
                return 'darkred';
              }
            }}
            nodeColor={(n: Node) => {
              if (n.className === 'active') {
                return 'green';
              } else {
                return 'red';
              }
            }}
            nodeStrokeWidth={3}
          />
          <Controls />
          <Background color='#aaa' gap={16} />
        </ReactFlow>
        <Button onClick={updateNetwork}>Update</Button>
      </VStack>
    </PageLayout>
  );
};

export default WorkflowPage;

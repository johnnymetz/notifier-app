import { useState, useMemo, forwardRef } from 'react';
import { toast } from 'react-toastify';
import Table from 'react-bootstrap/Table';
import Pagination from 'react-bootstrap/Pagination';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Dropdown from 'react-bootstrap/Dropdown';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import {
  faPencilAlt,
  faTrashAlt,
  faEllipsisV,
} from '@fortawesome/free-solid-svg-icons';
import { useTable, usePagination, useGlobalFilter } from 'react-table';

import useAuth from 'contexts/auth';
import apiClient from 'services/api';
// import { wait } from 'utils/helpers';
import EditEventModal from 'components/event/EditEventModal';
import ConfirmModal from 'components/widgets/ConfirmModal';

const GlobalFilter = ({ globalFilter, setGlobalFilter }) => {
  const [value, setValue] = useState(globalFilter);
  const onChange = async value => setGlobalFilter(value || undefined);
  return (
    <Form.Control
      value={value || ''}
      placeholder="Search"
      onChange={e => {
        setValue(e.target.value);
        onChange(e.target.value);
      }}
      data-test="all-events-list-search"
    />
  );
};

const CustomDropdownToggle = forwardRef(({ children, onClick }, ref) => (
  <div
    ref={ref}
    onClick={e => {
      e.preventDefault();
      onClick(e);
    }}
  >
    <Button variant="light" className="ellipsis-dropdown-toggle">
      {children}
    </Button>
  </div>
));

export default ({ events }) => {
  const { fetchUser } = useAuth();
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [showEditFormModal, setShowEditFormModal] = useState(false);
  const [showDeleteModal, setShowDeleteModal] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);

  const deleteEvent = async () => {
    setIsDeleting(true);
    // await wait(2000);
    const { error } = await apiClient.deleteEvent(selectedEvent.id);
    if (error) {
      console.error(error);
    } else {
      toast.success(`"${selectedEvent.name}" successfully deleted`);
      await fetchUser();
    }
    setIsDeleting(false);
    setShowDeleteModal(false);
  };

  const columns = useMemo(
    () => [
      {
        Header: 'Name',
        accessor: 'name',
      },
      {
        Header: 'Date',
        accessor: d => {
          const monthStr = d.annual_date.month.toString().padStart(2, 0);
          const dayStr = d.annual_date.day.toString().padStart(2, 0);
          const year = d.annual_date.year;
          return d.type === 'Birthday' || !year
            ? `${monthStr}-${dayStr}`
            : `${monthStr}-${dayStr}-${year}`;
        },
      },
      {
        Header: 'Age',
        accessor: d =>
          d.age !== null && d.age >= 0 ? (
            d.age
          ) : (
            <span title="Age unknown or event hasn't happened yet">
              &ndash;
            </span>
          ),
      },
      {
        Header: 'Type',
        accessor: 'type',
      },
      {
        Header: 'Actions',
        width: 70, // just large enough for 2 buttons with loading icon
        className: 'text-right',
        Cell: ({ row: { original } }) => {
          const event = {
            id: original.id,
            name: original.name,
            day: original.annual_date.day,
            month: original.annual_date.month,
            year: original.annual_date.year,
            type: original.type,
          };
          return (
            <div className="text-right">
              <Dropdown>
                <Dropdown.Toggle as={CustomDropdownToggle} alignRight>
                  <FontAwesomeIcon icon={faEllipsisV} size={'sm'} />
                </Dropdown.Toggle>

                <Dropdown.Menu>
                  <Dropdown.Item
                    onClick={() => {
                      setSelectedEvent(event);
                      setShowEditFormModal(true);
                    }}
                  >
                    <FontAwesomeIcon
                      icon={faPencilAlt}
                      size={'sm'}
                      style={{ marginRight: 8 }}
                    />{' '}
                    Edit
                  </Dropdown.Item>
                  <Dropdown.Item
                    onClick={() => {
                      setSelectedEvent(event);
                      setShowDeleteModal(true);
                    }}
                  >
                    <FontAwesomeIcon
                      icon={faTrashAlt}
                      size={'sm'}
                      style={{ marginRight: 10 }}
                    />{' '}
                    Delete
                  </Dropdown.Item>
                </Dropdown.Menu>
              </Dropdown>
            </div>
          );
        },
      },
    ],
    []
  );

  const {
    getTableProps,
    getTableBodyProps,
    headerGroups,
    prepareRow,
    rows,
    page, // rows for the active page

    // global filtering helpers
    setGlobalFilter,

    // pagination helpers
    canPreviousPage,
    canNextPage,
    pageOptions,
    pageCount,
    gotoPage,
    nextPage,
    previousPage,
    setPageSize,

    // state variables
    state: { pageIndex, pageSize, globalFilter },
  } = useTable(
    {
      columns,
      data: events,
      initialState: { pageSize: 5 },
    },
    useGlobalFilter,
    usePagination
  );

  return (
    <>
      {events.length === 0 ? (
        <div className="text-center mt-3">
          Add an event above to get started
        </div>
      ) : (
        <>
          <GlobalFilter
            globalFilter={globalFilter}
            setGlobalFilter={setGlobalFilter}
          />

          <Table
            striped
            hover
            responsive
            {...getTableProps()}
            data-test="all-events-list"
          >
            <thead>
              {headerGroups.map(headerGroup => (
                <tr {...headerGroup.getHeaderGroupProps()}>
                  {headerGroup.headers.map(column => {
                    return (
                      <th
                        {...column.getHeaderProps()}
                        width={column.width !== 150 ? column.width : null}
                        className=""
                      >
                        {column.render('Header')}
                      </th>
                    );
                  })}
                </tr>
              ))}
            </thead>
            <tbody {...getTableBodyProps()}>
              {page.map((row, i) => {
                prepareRow(row);
                return (
                  <tr {...row.getRowProps()}>
                    {row.cells.map(cell => {
                      return (
                        <td {...cell.getCellProps()}>{cell.render('Cell')}</td>
                      );
                    })}
                  </tr>
                );
              })}
            </tbody>
          </Table>

          <div className="d-flex justify-content-between">
            <Pagination>
              <Pagination.First
                onClick={() => gotoPage(0)}
                disabled={!canPreviousPage}
              />
              <Pagination.Prev
                onClick={() => previousPage()}
                disabled={!canPreviousPage}
              />
              <Pagination.Next
                onClick={() => nextPage()}
                disabled={!canNextPage}
              />
              <Pagination.Last
                onClick={() => gotoPage(pageCount - 1)}
                disabled={!canNextPage}
              />
            </Pagination>
            <div>
              <Form.Control
                as="select"
                value={pageSize}
                onChange={e => setPageSize(Number(e.target.value))}
                style={{ width: 120 }}
              >
                {[5, 10, 20, 40].map(size => (
                  <option key={size} value={size}>
                    Show {size}
                  </option>
                ))}
              </Form.Control>
            </div>
            <div className="d-none d-md-block">
              Page {pageIndex + 1} of {pageOptions.length || 1}{' '}
              <small className="text-muted" data-test="all-events-count">
                ({rows.length} records)
              </small>
            </div>
          </div>

          <EditEventModal
            showModal={showEditFormModal}
            setShowModal={setShowEditFormModal}
            eventValues={selectedEvent}
          />

          <ConfirmModal
            showModal={showDeleteModal}
            setShowModal={setShowDeleteModal}
            onConfirm={deleteEvent}
            title={'Delete Event?'}
            body={
              <span>
                Please confirm that you want to delete{' '}
                <b>{selectedEvent?.name}</b>.
              </span>
            }
            confirmButtonText={'Delete'}
            isSubmitting={isDeleting}
          />
        </>
      )}
    </>
  );
};

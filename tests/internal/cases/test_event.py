import uuid
import pytest
from unittest.mock import AsyncMock, patch
from sqlalchemy.ext.asyncio import AsyncSession

from src.internal.cases.event import create_event, get_event, get_all_events, update_event, delete_event
from src.internal.entities.event import CreateEvent, UpdateEvent
from src.db import models as m


@pytest.fixture
def mock_session():
    """Mock AsyncSession for testing."""
    session = AsyncMock(spec=AsyncSession)
    session.begin.return_value.__aenter__ = AsyncMock()
    session.begin.return_value.__aexit__ = AsyncMock(return_value=None)
    return session


@pytest.fixture
def sample_event():
    """Sample event data for testing."""
    return m.Event(
        id=uuid.uuid4(),
        name="Sample Event",
        info="This is a sample event",
        image_url="http://example.com/event.jpg",
        points=100,
        stand_id=uuid.uuid4()
    )


@pytest.fixture
def create_event_data():
    """Sample CreateEvent data."""
    return CreateEvent(
        name="Sample Event",
        info="This is a sample event",
        image_url="http://example.com/event.jpg",
        points=100,
        stand_id=uuid.uuid4()
    )


@pytest.fixture
def update_event_data():
    """Sample UpdateEvent data."""
    return UpdateEvent(
        name="Updated Event",
        info=None,
        image_url="http://example.com/updated_event.jpg",
        points=150,
        stand_id=None
    )


class TestCreateEvent:
    @pytest.mark.asyncio
    async def test_create_event_success(self, mock_session, sample_event, create_event_data):
        # Arrange
        with patch('internal.cases.event.e.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.create_event.return_value = sample_event
            mock_querier_class.return_value = mock_querier

            # Act
            result = await create_event(mock_session, create_event_data)

            # Assert
            assert result == sample_event
            mock_querier.create_event.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_event_failure(self, mock_session, create_event_data):
        # Arrange
        with patch('internal.cases.event.e.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.create_event.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await create_event(mock_session, create_event_data)

            # Assert
            assert result is None
            mock_querier.create_event.assert_called_once()


class TestGetEvent:
    @pytest.mark.asyncio
    async def test_get_event_success(self, mock_session, sample_event):
        # Arrange
        event_id = sample_event.id
        with patch('internal.cases.event.e.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_event_by_id.return_value = sample_event
            mock_querier_class.return_value = mock_querier

            # Act
            result = await get_event(mock_session, event_id)

            # Assert
            assert result == sample_event
            mock_querier.get_event_by_id.assert_called_once_with(id=event_id)

    @pytest.mark.asyncio
    async def test_get_event_not_found(self, mock_session):
        # Arrange
        event_id = uuid.uuid4()
        with patch('internal.cases.event.e.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_event_by_id.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await get_event(mock_session, event_id)

            # Assert
            assert result is None
            mock_querier.get_event_by_id.assert_called_once_with(id=event_id)


class TestGetAllEvents:
    @pytest.mark.asyncio
    async def test_get_all_events(self, mock_session, sample_event):
        # Arrange
        events = [sample_event]

        async def mock_async_iter():
            for event in events:
                yield event

        with patch('internal.cases.event.e.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_all_events = mock_async_iter
            mock_querier_class.return_value = mock_querier

            # Act
            result = []
            async for event in get_all_events(mock_session):
                result.append(event)

            # Assert
            assert result == events

    @pytest.mark.asyncio
    async def test_get_all_events_empty(self, mock_session):
        # Arrange
        async def mock_async_iter():
            return
            yield  # pragma: no cover

        with patch('internal.cases.event.e.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.get_all_events = mock_async_iter
            mock_querier_class.return_value = mock_querier

            # Act
            result = []
            async for event in get_all_events(mock_session):
                result.append(event)

            # Assert
            assert result == []


class TestUpdateEvent:
    @pytest.mark.asyncio
    async def test_update_event_success(self, mock_session, sample_event, update_event_data):
        # Arrange
        event_id = sample_event.id
        updated_event = m.Event(
            id=event_id,
            name="Updated Event",
            info=sample_event.info,
            image_url="http://example.com/updated_event.jpg",
            points=150,
            stand_id=sample_event.stand_id
        )
        with patch('internal.cases.event.e.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.update_event.return_value = updated_event
            mock_querier_class.return_value = mock_querier

            # Act
            result = await update_event(mock_session, event_id, update_event_data)

            # Assert
            assert result == updated_event
            mock_querier.update_event.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_event_not_found(self, mock_session, update_event_data):
        # Arrange
        event_id = uuid.uuid4()
        with patch('internal.cases.event.e.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.update_event.return_value = None
            mock_querier_class.return_value = mock_querier

            # Act
            result = await update_event(mock_session, event_id, update_event_data)

            # Assert
            assert result is None
            mock_querier.update_event.assert_called_once()


class TestDeleteEvent:
    @pytest.mark.asyncio
    async def test_delete_event_success(self, mock_session):
        # Arrange
        event_id = uuid.uuid4()
        with patch('internal.cases.event.e.AsyncQuerier') as mock_querier_class:
            mock_querier = AsyncMock()
            mock_querier.delete_event.return_value = None  # delete_event doesn't return anything in the code
            mock_querier_class.return_value = mock_querier

            # Act
            result = await delete_event(mock_session, event_id)

            # Assert
            assert result is True
            mock_querier.delete_event.assert_called_once_with(id=event_id)